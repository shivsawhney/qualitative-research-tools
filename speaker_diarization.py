input_path = "transcripts/MitaS_Transcript.txt"
output_path = "transcripts/labeled_MitaS_transcript.txt"

# Read the original transcript
with open(input_path, "r") as f:
    lines = f.read().split("\n\n")  # split on double newlines

# Speakers to alternate
speakers = ["SS", "MS"]

labeled_lines = []

# Add speaker label to each block
for i, block in enumerate(lines):
    block = block.strip()
    if block:  # skip if the block is just whitespace
        speaker = speakers[i % 2]
        labeled_block = f"{speaker}: {block}"
        labeled_lines.append(labeled_block)

# Join with double newlines again
final_text = "\n\n".join(labeled_lines)

# Save to a new file
with open(output_path, "w") as f:
    f.write(final_text)

print(f"Labeled transcript saved to: {output_path}")