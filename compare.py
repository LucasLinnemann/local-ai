import requests

URL = "http://localhost:1234/v1/embeddings"
MODEL = "text-embedding-nomic-embed-text-v1.5"


def embed(text):
    response = requests.post(URL, json={"model": MODEL, "input": text}, timeout=60)
    return response.json()["data"][0]["embedding"]


def similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    length_a = sum(x * x for x in a) ** 0.5
    length_b = sum(y * y for y in b) ** 0.5
    return dot / (length_a * length_b)


question = "How much time off do I get?"
chunks = [
    "Northwind Tooling employees receive 17 PTO days per year.",
    "Requests must be submitted 9 days in advance.",
    "The spindle torque spec is 45 newton meters.",
    "Coolant is changed every 30 days.",
]

q = embed("search_query: " + question)
for chunk in chunks:
    score = similarity(q, embed("search_document: " + chunk))
    print(round(score, 3), chunk)