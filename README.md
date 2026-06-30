# Qualitative Research Tools

A collection of lightweight Python scripts that automate repetitive tasks in qualitative research while leaving interpretation and analysis to the researcher.

## Philosophy

This repository is designed to support, not replace, the qualitative research process. The scripts automate mechanical tasks such as transcription, organization, and documentation while preserving researcher judgment during coding and analysis.

## Features

### `transcribe.py`
Transcribe audio interviews into text using OpenAI's Whisper.

Example:

```bash
python scripts/transcribe.py audio/interview.mp3
```

---

### `manually_code_transcript.py`
Code transcripts sentence-by-sentence using a customizable codebook.

Outputs:
- CSV of coding decisions
- Highlighted Word document

Example:

```bash
python scripts/manually_code_transcript.py transcripts/interview.txt \
    --codebook scripts/codebook.csv \
    --out-dir codeds
```

---

### `organize_quotes.py`
Combine coded transcripts into analysis-ready outputs.

Outputs:
- Markdown quote packet grouped by theme
- Interview × theme matrix
- Overall theme frequency table

Example:

```bash
python scripts/organize_quotes.py codeds --out-dir outputs
```

## Installation

Clone the repository and install the required packages:

```bash
git clone https://github.com/shivsawhney/qualitative-research-tools.git
cd qualitative-research-tools

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```
