import requests
from chunk import load_chunks

LM = "http://localhost:1234/v1"
QDRANT = "http://localhost:6333"
EMBED_MODEL = "text-embedding-nomic-embed-text-v1.5"


def embed(text):
    response = requests.post(
        f"{LM}/embeddings",
        json={"model": EMBED_MODEL, "input": text},
        timeout=60,
    )
    return response.json()["data"][0]["embedding"]


points = []
for number, chunk in enumerate(load_chunks()):
    points.append({
        "id": number,
        "vector": embed("search_document: " + chunk),
        "payload": {"text": chunk},
    })

requests.delete(f"{QDRANT}/collections/docs", timeout=60)
requests.put(
    f"{QDRANT}/collections/docs",
    json={"vectors": {"size": 768, "distance": "Cosine"}},
    timeout=60,
)

response = requests.put(
    f"{QDRANT}/collections/docs/points?wait=true",
    json={"points": points},
    timeout=60,
)
print(response.json())
print(f"Saved {len(points)} chunks")
