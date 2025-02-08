import datetime
from pathlib import Path
from openai import OpenAI
client = OpenAI()

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
speech_file_path = Path(__file__).parent / f"speech-{timestamp}.mp3"
response = client.audio.speech.create(
  model="tts-1-hd",
  voice="echo",
  input=""
)

response.stream_to_file(speech_file_path)
