import chromadb
from sentence_transformers import SentenceTransformer
from loader import load_docs
from chunker import chunk_doc
docs=load_docs("k8s-website/content/en/docs/concepts")
chunks = []
for d in docs:
    for c in chunk_doc(d):
        chunks.append(c)
model = SentenceTransformer("all-MiniLM-L6-v2")
vecs = model.encode([c["text"] for c in chunks], normalize_embeddings=True, show_progress_bar=True)
client = chromadb.PersistentClient(path="chroma_db")
try:
    client.delete_collection("k8s")
except Exception:
    pass
col = client.create_collection("k8s", metadata={"hnsw:space": "cosine"})
col.add(
    ids=[str(i) for i in range(len(chunks))],
    embeddings=vecs.tolist(),
    documents=[c["text"] for c in chunks],
    metadatas=[{"path": c["path"]} for c in chunks],
)
print("stored", col.count(), "chunks")