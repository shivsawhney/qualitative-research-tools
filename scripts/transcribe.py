import whisper
import os 
from pathlib import Path


print("Loading model...")
model = whisper.load_model("base")

input_file = Path(input("Enter path to audio file: ").strip())
output_file = Path(input("Enter path to save transcript: ").strip())

result = model.transcribe(str(input_file))

output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(result["text"])

print(f"Transcript saved to: {output_file}")