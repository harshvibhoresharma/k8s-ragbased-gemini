import re
from loader import load_docs
def clean(text):
    text = re.sub(r"^---.*?---\s*", "", text, flags=re.S) 
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)    
    text = re.sub(r"\{\{.*?\}\}", "", text, flags=re.S)  
    return text
def chunk_doc(doc,max_words=200,overlap=30):
    text=clean(doc["text"])
    sections = re.split(r"\n(?=#{1,3} )", text)
    chunks = []
    for sec in sections:
        words=sec.split()
        if len(words)<20:
            continue
        step = max_words-overlap
        for i in range(0,len(words),step):
            chunks.append({
                "path": doc["path"],
                "text": " ".join(words[i:i + max_words]),
            })
    return chunks
if __name__ == "__main__":
    docs = load_docs("k8s-website/content/en/docs/concepts")
    all_chunks = [c for d in docs for c in chunk_doc(d)]
    print(len(all_chunks), "chunks")
    print(all_chunks[50]["path"])
    print(all_chunks[50]["text"])