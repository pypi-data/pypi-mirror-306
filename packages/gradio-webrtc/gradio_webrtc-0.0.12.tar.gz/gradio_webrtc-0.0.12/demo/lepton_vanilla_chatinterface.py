import gradio as gr
from gradio_webrtc import WebRTC, ReplyOnPause, AdditionalOutputs
import numpy as np
import io
from pydub import AudioSegment
import openai
import time
import base64
import os

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

if account_sid and auth_token:
    from twilio.rest import Client
    client = Client(account_sid, auth_token)

    token = client.tokens.create()

    rtc_configuration = {
        "iceServers": token.ice_servers,
        "iceTransportPolicy": "relay",
    }
else:
    rtc_configuration = None


def create_client(api_key):
    return openai.OpenAI(
        base_url="https://llama3-1-8b.lepton.run/api/v1/",
        api_key=api_key
    )


def update_or_append_conversation(conversation, id, role, content):
    # Find if there's an existing message with the given id
    for message in conversation:
        if message.get("id") == id and message.get("role") == role:
            message["content"] = content
            return
    # If not found, append a new message
    conversation.append({"id": id, "role": role, "content": content})
    

def response(prompt: str, lepton_conversation: list[dict],
             gradio_conversation: list[dict], client: openai.OpenAI, output_format: str):
    
    if client is None:
        raise gr.Error("Please enter a valid API key first.")

    bitrate = 128 if output_format == "mp3" else 32  # Higher bitrate for MP3, lower for OPUS

    stream = client.chat.completions.create(
        model="llama3.1-8b",
        messages=lepton_conversation + [{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1028,
        stream=True,
    )

    id = str(time.time())
    update_or_append_conversation(lepton_conversation, id, "user", prompt)
    update_or_append_conversation(gradio_conversation, id, "user", prompt)
    full_response = ""

    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        content = delta.content

        if content:
            full_response += content
            update_or_append_conversation(lepton_conversation, id, "assistant", full_response)
            update_or_append_conversation(gradio_conversation, id, "assistant", full_response)
            yield gr.skip(), gradio_conversation
    yield lepton_conversation, gradio_conversation


def set_api_key(api_key):
    if not api_key:
        raise gr.Error("Please enter a valid API key.")
    client = create_client(api_key)
    gr.Info("Set API Key Successfully", duration=5)
    return client, gr.skip()


with gr.Blocks() as demo:
    with gr.Group():
        with gr.Row():
            chatbot = gr.Chatbot(label="Conversation", type="messages")
        with gr.Row(equal_height=True):
            with gr.Column(scale=1):
                format_dropdown = gr.Dropdown(choices=["mp3", "opus"], value="mp3", label="Output Audio Format")
                api_key_input = gr.Textbox(type="password", label="Enter your Lepton API Key")
                set_key_button = gr.Button("Set API Key", variant="primary")
            with gr.Column(scale=3):
                textbox = gr.Textbox(label="API Key")

    client_state = gr.State(None)
    lepton_conversation = gr.State([])

    set_key_button.click(set_api_key, inputs=[api_key_input], outputs=[client_state, set_key_button])
    textbox.submit(response, inputs=[textbox, lepton_conversation, chatbot, client_state, format_dropdown],
                   outputs=[lepton_conversation, chatbot])
    # audio.stream(
    #     ReplyOnPause(response),
    #     inputs=[audio, lepton_conversation, chatbot, client_state, format_dropdown],
    #     outputs=[audio]
    # )
    # audio.on_additional_outputs(lambda l, g: (l, g), outputs=[lepton_conversation, chatbot],
    #                             show_progress="hidden", queue=False)

    demo.launch()
