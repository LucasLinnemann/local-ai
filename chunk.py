from pathlib import Path


def chunk_file(path):
    text = path.read_text()
    pieces = text.split("\n## ")
    title = pieces[0].strip()

    chunks = []
    for piece in pieces[1:]:
        chunks.append(f"{title}\n## {piece.strip()}")
    return chunks


def load_chunks():
    all_chunks = []
    for path in sorted(Path("docs").rglob("*.md")):
        all_chunks.extend(chunk_file(path))
    return all_chunks


if __name__ == "__main__":
    for number, chunk in enumerate(load_chunks()):
        print(f"--- chunk {number} ---")
        print(chunk)