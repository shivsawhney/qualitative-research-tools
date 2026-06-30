import whisper
import os 
from pathlib import Path
import argparse

"""
transcribe.py

Transcribe an audio file into plain text using OpenAI Whisper.

This script converts spoken audio into a text transcript while preserving the
original wording. It is intended to automate the transcription step of the
qualitative research workflow without performing interpretation or analysis.

Example:
    python scripts/transcribe.py audio/interview1.mp3
    python scripts/transcribe.py audio/interview1.mp3 transcripts/interview1.txt
"""

def transcribe(input_path: Path, output_path: Path, model_name: str = "base"):
    print(f"Loading {model_name} Whisper model...")
    model = whisper.load_model(model_name)

    print(f"Transcribing {input_path.name}...")
    result = model.transcribe(str(input_path))

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
         f.write(result["text"].strip())

    print(f"Transcript saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe an audio file using OpenAI Whisper."
    )

    parser.add_argument(
        "input_file",
        help="Path to input audio file"
    )

    parser.add_argument(
        "output_file",
        nargs="?",
        help="Path to save transcript. Default is audio file name with txt extension"
    )

    parser.add_argument(
        "--model",
        default="base",
        help="Whisper model to use (tiny, base, small, medium, large)"  
    )

    args = parser.parse_args()

    input_path = Path(args.input_file)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if args.output_file:
        output_path = Path(args.output_file)
    else:
        output_path = input_path.with_suffix(".txt")

    transcribe(input_path, output_path, args.model)

if __name__ == "__main__":
    main()
