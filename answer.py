import os
import chromadb
from sentence_transformers import SentenceTransformer
from google import genai

model = SentenceTransformer("all-MiniLM-L6-v2")
col = chromadb.PersistentClient(path="chroma_db").get_collection("k8s")
llm = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def retrieve(question, n=4):
    qv = model.encode([question], normalize_embeddings=True).tolist()
    res = col.query(query_embeddings=qv, n_results=n)
    chunks = []
    for i in range(len(res["documents"][0])):
        chunks.append({
            "text": res["documents"][0][i],
            "path": res["metadatas"][0][i]["path"],
        })
    return chunks

def build_prompt(question, chunks):
    context = ""
    for c in chunks:
        context += "Source: " + c["path"] + "\n" + c["text"] + "\n\n"
    return (
        "Answer the question using ONLY the context below. "
        "If the context doesn't contain the answer, say you don't know.\n\n"
        "Context:\n" + context +
        "Question: " + question
    )

while True:
    q = input("\nQuestion (or quit): ")
    if q == "quit":
        break
    chunks = retrieve(q)
    prompt = build_prompt(q, chunks)
    reply = llm.models.generate_content(model="gemini-3.8-flash", contents=prompt)
    print("\n" + reply.text)
    print("\nSources:")
    for c in chunks:
        print("-", c["path"])