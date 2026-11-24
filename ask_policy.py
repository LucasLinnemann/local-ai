import requests

POLICY = "Northwind Tooling employees receive 17 PTO days per year. Requests must be submitted 9 days in advance. Unused days do not carry over."

URL = "http://localhost:1234/v1/chat/completions"

payload = {
    "model": "google/gemma-4-26b-a4b-qat",
    "messages": [
        {"role": "system", "content": "Answer using the Policy provided."},
        {"role": "user", "content": f"POLICY: {POLICY}\n\nQUESTION: How many PTO days do Northwind Tooling employees receive per year?"},
    ],
    "temperature": 0.2,
}

response = requests.post(URL, json=payload, timeout=120)
data = response.json()
print(data["choices"][0]["message"]["content"])
