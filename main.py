from sentence_transformers import SentenceTransformer
import numpy as np
text = """
Kubernetes is an open-source system for automating deployment, scaling, and management of containerized applications.
A Pod is the smallest deployable unit in Kubernetes. It can hold one or more containers that share storage and network.
A Deployment manages a set of identical Pods. It makes sure the desired number of replicas are running and handles rolling updates.
A Service gives a stable IP address and DNS name to a group of Pods, so other apps can reach them even when Pods are replaced.
KEDA is a Kubernetes component that scales workloads based on events, like the number of messages in a queue. It can scale a Deployment down to zero when there is no work.
ConfigMaps store non-secret configuration data as key-value pairs. Secrets store sensitive data like passwords and API keys.
"""

def chunk(text,size=30):
    words=text.split()
    chunks=[]
    for i in range(0,len(words),size):
        piece=words[i:i+size]
        chunks.append(" ".join(piece))
    return chunks
chunks=chunk(text)
print(f"Made {len(chunks)} chunks\n")
model = SentenceTransformer("all-MiniLM-L6-v2")
chunk_vecs=model.encode(chunks,normalize_embeddings=True)
question="What is Kubernetes?"
q_vec = model.encode([question], normalize_embeddings=True)[0]
scores=chunk_vecs @ q_vec
for i in np.argsort(scores)[::-1][:3]:
    print(round(float(scores[i]), 3), "|", chunks[i], "\n")
