import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
col = chromadb.PersistentClient(path="chroma_db").get_collection("k8s")

while True:
    q = input("\nQuestion (or quit): ")
    if q == "quit":
        break
    qv = model.encode([q], normalize_embeddings=True).tolist()
    res = col.query(query_embeddings=qv, n_results=3)
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        print(round(1 - dist, 3), meta["path"])
        print(doc[:300], "\n")