import requests

URL = "http://localhost:1234/v1/chat/completions"

payload = {
    "model": "google/gemma-4-26b-a4b-qat",
    "messages": [
        {"role": "system", "content": "Answer in two sentences."},
        {"role": "user", "content": "What is a Kubernetes pod?"},
    ],
    "temperature": 0.2,
}

response = requests.post(URL, json=payload, timeout=120)
data = response.json()
print(data["choices"][0]["message"]["content"])
