import os
import base64
import openai

client = openai.OpenAI(
  base_url="https://llama3-2-3b.lepton.run/api/v1/",
  api_key="r5zhL9iWWGpqDbb2Z6f0EsG1Yb1Hreog"
)

format_ = "mp3"
bitrate = 128

# calls the api
completion = client.chat.completions.create(
  model="llama3.2-3b",
  # This specifies what audio input and output should be
  extra_body={
    # input formats
    "tts_audio_format": format_,
    "tts_audio_bitrate": bitrate,
    # output formats
    "require_audio": True,
    "tts_preset_id": "jessica",
  },
  # this gets you audio input
  messages=[
      {"role": "user", "content": "Which is better Chicago style or New York style pizza?"},
  ],
  max_tokens=128,
  stream=True,
)

# Get both text and audios
audios = []
for chunk in completion:
  if not chunk.choices:
    continue
  content = chunk.choices[0].delta.content
  audio = getattr(chunk.choices[0], 'audio', [])
  if content:
    print(content, end="")
  if audio:
    audios.extend(audio)

buf = b''.join([base64.b64decode(audio) for audio in audios[:]])
with open('output.mp3', 'wb') as f:
  f.write(buf)

print("\nAudio saved to output.mp3")