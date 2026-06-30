import argparse
from pathlib import Path
import pandas as pd

"""
organize_quotes.py

Organize manually coded qualitative research data into analysis-ready outputs.

This script reads one or more coding decision CSVs, combines them into a
single dataset, and generates summaries to support qualitative analysis.
Outputs include:
    - A Markdown quote packet grouped by theme.
    - An interview-by-theme frequency matrix.
    - Overall theme counts across all interviews.

Example:
    python scripts/organize_quotes.py codeds --out-dir outputs
"""

def load_coding_files(input_dir: Path) -> pd.DataFrame:
    """Read all CSV files in a directory and combine them into one DataFrame."""
    csv_paths = sorted(input_dir.glob("*.csv"))

    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found in: {input_dir}")

    frames = []

    for path in csv_paths:
        df = pd.read_csv(path)

        if "source_file" not in df.columns:
            df["source_file"] = path.stem.replace("_coding_decisions", "")

        frames.append(df)

    return pd.concat(frames, ignore_index=True)

def clean_quotes(df: pd.DataFrame, include_none: bool = False) -> pd.DataFrame:
    """Remove uncoded rows unless the user wants to include them."""
    required_columns = {"source_file", "sentence_id", "text", "theme_code", "theme_name"}

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if not include_none:
        df = df[df["theme_code"] != 0]

    return df.copy()

def write_quote_packet(df: pd.DataFrame, output_path: Path) -> None:
    """Write a Markdown file with quotes grouped by theme."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    theme_counts = df["theme_name"].value_counts()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Quote Packet\n\n")
        f.write(f"Total quotes: {len(df)}\n\n")

        f.write("## Theme Counts\n\n")
        for theme, count in theme_counts.items():
            f.write(f"- {theme}: {count}\n")

        f.write("\n---\n\n")

        for theme, group in df.groupby("theme_name"):
            f.write(f"## {theme}\n\n")
            f.write("### Researcher memo\n\n")
            f.write("_What patterns, tensions, exceptions, or questions do these quotes raise?_\n\n")

            f.write("| Interview | Sentence ID | Quote |\n")
            f.write("|---|---:|---|\n")

            for _, row in group.iterrows():
                quote = str(row["text"]).replace("\n", " ").replace("|", "\\|")
                source = row["source_file"]
                sentence_id = row["sentence_id"]

                f.write(f"| {source} | {sentence_id} | {quote} |\n")

            f.write("\n---\n\n")

def write_theme_matrix(df: pd.DataFrame, output_path: Path) -> None:
    """Write interview-by-theme count matrix."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    matrix = pd.crosstab(df["source_file"], df["theme_name"])
    matrix.to_csv(output_path)


def write_theme_counts(df: pd.DataFrame, output_path: Path) -> None:
    """Write total theme counts."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    counts = df["theme_name"].value_counts().reset_index()
    counts.columns = ["theme_name", "quote_count"]
    counts.to_csv(output_path, index=False)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Organize coded quotes into analysis-ready outputs."
    )

    parser.add_argument(
        "input_dir",
        help="Directory containing coded CSV files.",
    )

    parser.add_argument(
        "--out-dir",
        default="outputs",
        help="Directory where outputs will be saved.",
    )

    parser.add_argument(
        "--include-none",
        action="store_true",
        help="Include rows coded as NONE.",
    )

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    out_dir = Path(args.out_dir)

    df = load_coding_files(input_dir)
    df = clean_quotes(df, include_none=args.include_none)

    quote_packet_path = out_dir / "quote_packet.md"
    theme_matrix_path = out_dir / "theme_matrix.csv"
    theme_counts_path = out_dir / "theme_counts.csv"

    write_quote_packet(df, quote_packet_path)
    write_theme_matrix(df, theme_matrix_path)
    write_theme_counts(df, theme_counts_path)

    print("Done.")
    print(f"Saved: {quote_packet_path}")
    print(f"Saved: {theme_matrix_path}")
    print(f"Saved: {theme_counts_path}")


if __name__ == "__main__":
    main()