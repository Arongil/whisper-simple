import os
import sys
import json
from openai import OpenAI
client = OpenAI()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please pass in a directory with mp3 files to transcribe.")
        exit()

    for dirname in sys.argv[1:]:
        filenames = os.listdir(dirname)
        for filename in filenames:
            root, ext = os.path.splitext(filename)
            if ext.lower() != ".mp3" or f"{root}-plaintext.txt" in filenames:
                continue  # either not an mp3 or file has already been converted

            audio_file = open(f"{dirname}/{filename}", "rb")
            transcription = client.audio.transcriptions.create(
              model="whisper-1", 
              file=audio_file, 
              response_format="verbose_json",
              timestamp_granularities=["segment"],
              prompt="Hello, this is an interview about AI.",  # demonstrate good output since there is no instruction fine-tuning
            )

            txt = ""
            timestamped_txt = ""
            for segment in transcription.segments:
                if segment['text'] == "":
                    continue
                start_time = round(segment["start"])
                minutes, seconds = start_time // 60, start_time % 60
                silent_or_failed = segment["no_speech_prob"] > 1 or segment["avg_logprob"] < -1
                timestamped_txt += f"{minutes:02d}:{seconds:02d}"
                timestamped_txt += f" - SILENT OR COULD NOT TRANSCRIBE" if silent_or_failed else ""
                timestamped_txt += f"\n{segment['text'].strip()}\n\n"
                txt += segment['text'].strip() + ("\n\n" if segment['text'][-1] in ['.', '?', '!'] else " ")

            with open(f"{dirname}/{root}-timestamped.txt", "w") as f:
                f.write(timestamped_txt)
            with open(f"{dirname}/{root}-plaintext.txt", "w") as f:
                f.write(txt)
            with open(f"{dirname}/{root}-transcript.json", "w") as f:
                json.dump(transcription.segments, f)
