from pathlib import Path
from docx import Document
import argparse
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


"""
semantic_search.py

Search .docx transcripts by meaning using sentence embeddings.

Example:
    python scripts/semantic_search.py "school leadership decisions" transcripts --top 4
"""

BOLD = "\033[1m"
RESET = "\033[0m"

def read_docx(path: Path) -> str:
    """Read paragraph text from a Word document."""
    doc = Document(path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)

def split_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    cleaned_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if sentence:
            cleaned_sentences.append(sentence)

    return cleaned_sentences

def build_sentence_dictionary(folder: Path) -> list[dict]:
    """Build searchable sentence records from all .docx files in a folder."""
    records = []

    for docx_file in sorted(folder.glob("*.docx")):
        text = read_docx(docx_file)
        sentences = split_sentences(text)

        for i, sentence in enumerate(sentences):
            before = sentences[i - 1] if i > 0 else ""
            after = sentences[i + 1] if i < len(sentences) - 1 else ""

            records.append(
                {
                    "source_file": docx_file.stem,
                    "sentence_id": i + 1,
                    "sentence": sentence,
                    "before": before,
                    "after": after,
                }
            )

    return records


def semantic_search(
    query: str,
    records: list[dict],
    model: SentenceTransformer,
    top_n: int,
) -> list[dict]:
    """Return the top semantic matches for a query."""
    if not records:
        return []

    query_embedding = model.encode(query)
    sentences = [record["sentence"] for record in records]
    sentence_embeddings = model.encode(sentences)

    scores = cosine_similarity([query_embedding], sentence_embeddings)[0]

    for record, score in zip(records, scores):
        record["score"] = float(score)

    ranked = sorted(records, key=lambda x: x["score"], reverse=True)
    return ranked[:top_n]


def print_results(results: list[dict]) -> None:
    """Print search results with context."""
    if not results:
        print("No results found.")
        return

    for result in results:
        print("=" * 80)
        print(f"Transcript: {result['source_file']}")
        print(f"Sentence #: {result['sentence_id']}")
        print(f"Similarity: {result['score']:.3f}")
        print()

        if result["before"]:
            print(result["before"])

        print(f"{BOLD}{result['sentence']}{RESET}")

        if result["after"]:
            print(result["after"])

        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search .docx transcripts semantically using sentence embeddings."
    )

    parser.add_argument(
        "query",
        help="Search query, e.g. 'school leadership decisions'.",
    )

    parser.add_argument(
        "folder",
        help="Folder containing .docx transcript files.",
    )

    parser.add_argument(
        "--top",
        type=int,
        default=4,
        help="Number of results to show. Default: 4.",
    )

    parser.add_argument(
        "--model",
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="SentenceTransformer model to use.",
    )

    args = parser.parse_args()

    folder = Path(args.folder)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    print("Loading model...")
    model = SentenceTransformer(args.model)

    print("Building search corpus...")
    records = build_sentence_dictionary(folder)

    print(f"Searching {len(records)} sentences...")
    results = semantic_search(args.query, records, model, args.top)

    print_results(results)


if __name__ == "__main__":
    main()