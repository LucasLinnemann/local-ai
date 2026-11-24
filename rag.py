import requests
import time

BASE = "http://localhost:1234/v1"
EMBED_MODEL = "text-embedding-nomic-embed-text-v1.5"
CHAT_MODEL = "google/gemma-4-26b-a4b-qat"
QDRANT = "http://localhost:6333"

def embed(text):
    response = requests.post(
        f"{BASE}/embeddings",
        json={"model": EMBED_MODEL, "input": text},
        timeout=60,
    )
    return response.json()["data"][0]["embedding"]


def similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    length_a = sum(x * x for x in a) ** 0.5
    length_b = sum(y * y for y in b) ** 0.5
    return dot / (length_a * length_b)


def search(question, top=2):
    q = embed("search_query: " + question)
    response = requests.post(
        f"{QDRANT}/collections/docs/points/query",
        json={"query": q, "limit": top, "with_payload": True},
        timeout=60,
    )
    points = response.json()["result"]["points"]
    return [point["payload"]["text"] for point in points]


def answer(question):
    start = time.time()
    found = search(question)
    search_seconds = time.time() - start

    context = "\n".join(found)
    payload = {
        "model": CHAT_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Answer using only the context provided. "
                "If the context does not contain the answer, say you don't know. "
                "You may do simple math on numbers from the context.",
            },
            {
                "role": "user",
                "content": f"CONTEXT:\n{context}\n\nQUESTION: {question}",
            },
        ],
        "temperature": 0.2,
        "reasoning_effort": "none",
    }
    start = time.time()
    response = requests.post(f"{BASE}/chat/completions", json=payload, timeout=120)
    answer_seconds = time.time() - start

    print(f"\nSearch took {search_seconds:.2f}s, answer took {answer_seconds:.2f}s")
    print(response.json()["usage"])
    return found, response.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    question = input("Question: ")
    found, reply = answer(question)
    print("\nRetrieved:")
    for chunk in found:
        print(" -", chunk)
    print("\nAnswer:", reply)