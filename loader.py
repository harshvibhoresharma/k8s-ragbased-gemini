from pathlib import Path

def load_docs(root):
    docs=[]
    for p in Path(root).rglob("*.md"):
        docs.append({"path":str(p),
                     "text":p.read_text(encoding="utf-8")})
    return docs
if __name__ == "__main__":
    docs = load_docs("k8s-website/content/en/docs/concepts")
    print(len(docs), "files loaded")
    print(docs[0]["path"])
    print(docs[0]["text"][:500])