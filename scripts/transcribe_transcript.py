import whisper
import os 
import time
from pathlib import Path

start = time.time()

print("Loading model...")
model = whisper.load_model("base")  # or "medium" or "base"

audio_folder = "/Users/Shiv/Desktop/Thesis/Interviews"
output_folder = "/Users/Shiv/Desktop/Thesis/Transcripts"
filename = "Susan_P_Interview.m4a"
filepath = os.path.join(audio_folder, filename)

print("Transcribing...")
result = model.transcribe(filepath)

print("Done in", round(time.time() - start, 2), "seconds")

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

output_path = os.path.join(output_folder, "Mita_s.txt")
with open(output_path, "w") as f:
    f.write(result["text"])

#to use this, first set cd to transcriber, then activate virtual environment
#command to run is python kahaniyan.py