# local-ai

A small retrieval-augmented generation (RAG) pipeline that runs fully on one machine: a local model in LM Studio, a Qdrant vector store in Docker, and plain Python with `requests`. No cloud API, no framework.

This is a learning project. I built it step by step to understand each part of RAG by writing it myself, then measured it with an eval set.

## How it works

**Load time (once, and again whenever a document changes):**

1. `chunk.py` splits each Markdown file in `docs/` on its `##` headings and puts the document title on every chunk.
2. `load.py` embeds each chunk, rebuilds the Qdrant collection, and saves the chunks with their vectors.

**Question time (every question):**

1. `rag.py` embeds the question (one embedding call).
2. Qdrant returns the two closest chunks.
3. The chat model answers using only those chunks, and says "I don't know" when they do not contain the answer.

The documents in `docs/` are made up (a fictional company, Northwind Tooling). Both have a "Carryover" section on purpose, to test that the search can tell two documents apart when the headings match.

## Files

| File | What it does |
|---|---|
| `ask.py` | First call to the local model |
| `ask_policy.py` | Adds a system message and a prompt built from a document |
| `compare.py` | Embeddings and cosine similarity written by hand |
| `chunk.py` | Splits documents into chunks |
| `load.py` | Embeds chunks and saves them to Qdrant, safe to re-run |
| `rag.py` | Search plus answer, with timing and token usage |
| `eval.py` | 20 test questions with expected answers, prints a score |

## Run it

Needs LM Studio with its local server on port 1234, Docker, and `uv`.

Models used: `google/gemma-4-26b-a4b-qat` for chat and `text-embedding-nomic-embed-text-v1.5` for embeddings.

```bash
docker run -d --name qdrant -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant
uv run --with requests python load.py
uv run --with requests python rag.py
uv run --with requests python eval.py
```

## What I measured

Hardware: a mini PC with a Ryzen AI Max+ 395 and 32 GB of memory assigned to the integrated GPU. The chat model runs at about 60 tokens per second.

### Reasoning on or off

Same 20 questions, one run each:

| | Reasoning off | Reasoning on |
|---|---|---|
| Score | 19 of 20 | 17 of 20 |
| Whole run | about 8 s | about 97 s |
| Tokens written per answer | 7 to 19 | 136 to 2,037 |

Two of the three failures with reasoning on were the grader, not the model: the answers were correct but did not contain the literal "yes" or "no" the check looks for. Real accuracy was the same, at about 12 times the cost in time. For lookup questions over short chunks, reasoning stays off.

### One question that needed two fixes

A question asking for PTO days plus sick days kept failing. Changing one thing at a time showed why:

| | Vague question | Clear question |
|---|---|---|
| Strict prompt ("answer using only the context") | lists 17 and 6 | "I don't know" |
| Prompt that also allows simple math | lists 17 and 6 | **23** |

The sum is not written anywhere in the documents, so a strict prompt blocks it. It took both a clearly worded question and one added sentence in the system message. The four "not in the documents" questions still got "I don't know" afterwards.

### Other findings

- Answer time is close to tokens written divided by tokens per second. Most of the original 4.4 s per answer was hidden reasoning tokens.
- An early 19 s per question was LM Studio swapping the chat and embedding models in and out of memory, not the search. Keeping both loaded brought search to 0.02 s.
- Re-running the loader after deleting a section used to leave the old chunk behind, still searchable. The loader now rebuilds the collection so the store always matches the documents.

## Known limits

- The eval check is a simple "does the answer contain this text", so it can pass or fail for the wrong reason.
- 20 questions over two short documents, one run per setting. Enough to choose settings for this setup, not a general result.

## Next

- Tighter eval checks
- A first tool call
- The same pipeline on pgvector