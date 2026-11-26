# Kubernetes Docs RAG (Gemini)

A "chat with the docs" bot built from scratch. Ask a question about Kubernetes and it finds the most relevant parts of the official docs, then uses Gemini to write an answer from them and list the source files.

## How it works

1. `loader.py` reads the Kubernetes markdown docs.
2. `chunker.py` cleans the text and splits it by heading into ~200-word chunks with overlap.
3. `index.py` embeds every chunk with `all-MiniLM-L6-v2` and stores them in ChromaDB (local).
4. `answer.py` embeds your question, retrieves the top chunks, and sends them to Gemini with the instruction to answer only from that context.

`search.py` is a retrieval-only version, handy for checking which chunks come back.

## Tech

Python, sentence-transformers, ChromaDB, Google Gemini API. No LangChain, everything is hand-built.

## Setup

```bash
git clone https://github.com/harshvibhoresharma/k8s-ragbased-gemini.git
cd k8s-ragbased-gemini
python -m venv venv
venv\Scripts\activate
pip install sentence-transformers numpy chromadb google-genai
```

Get the docs (only the concepts section):

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/kubernetes/website.git k8s-website
cd k8s-website
git sparse-checkout set content/en/docs/concepts
cd ..
```

## Run

```bash
python index.py          # build the vector DB (once)
$env:GEMINI_API_KEY="your_key"
python answer.py         # ask questions
```

Get a free API key at [aistudio.google.com](https://aistudio.google.com).

## Known issues / next steps

- Some chunks are just "What's next" link lists and add noise.
- Only the concepts docs are indexed, so how-to questions are weak.
- Planned: hybrid search, reranking, and a test set to measure retrieval.
