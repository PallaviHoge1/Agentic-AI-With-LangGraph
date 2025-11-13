# src/rag_query.py
import faiss, pickle
from sentence_transformers import SentenceTransformer
import subprocess, json
import numpy as np

import subprocess

# def call_ollama(prompt, model="llama3.2b"):
#     cmd = ["ollama", "run", model]
#     p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     out, err = p.communicate(prompt)
#     if p.returncode != 0:
#         raise RuntimeError(f"Ollama run failed: {err}")
#     return out

model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve(query, k=3):
    with open("data/faiss_meta.pkl","rb") as f:
        meta = pickle.load(f)
    idx = faiss.read_index("data/faiss_index.idx")
    q_emb = model.encode([query])[0].astype('float32')
    D, I = idx.search(np.array([q_emb]), k)
    docs = [meta['docs'][i] for i in I[0]]
    return docs

# def call_ollama(prompt):
#     # Uses ollama CLI
#     # Adjust the model name to the one you have: e.g. 'llama3-3b' or as shown by ollama list
#     cmd = ["ollama","run","llama3.2b","--prompt", prompt]
#     res = subprocess.run(cmd, capture_output=True, text=True)
#     return res.stdout

# src/rag_query.py (update or replace call_ollama)
import subprocess

def call_ollama(prompt, model="llama3.2:3b", timeout=None):
    """
    Calls ollama run <model> and sends the prompt via stdin.
    Returns stdout string on success or raises RuntimeError with stderr.
    """
    cmd = ["ollama", "run", model]
    try:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = p.communicate(prompt, timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill()
        out, err = p.communicate()
        raise RuntimeError(f"Ollama call timed out. Stderr: {err}")

    if p.returncode != 0:
        raise RuntimeError(f"Ollama returned non-zero exit code {p.returncode}. Stderr:\n{err}")

    if not out.strip():
        # no stdout returned
        raise RuntimeError(f"Ollama returned empty output. Stderr:\n{err}")

    return out

def answer(query, model="llama3.2:3b", top_k=4):
    docs = retrieve(query, k=top_k)
    retrieved = "\n\n".join(docs)
    prompt = (
        "You are an assistant helping a clothing store owner. Use only the information below.\n\n"
        f"Retrieved context:\n{retrieved}\n\nUser question: {query}\n\n"
        "Answer concisely (1) competitor list, (2) busiest hour summary, (3) 3 actionable recommendations."
    )
    return call_ollama(prompt, model=model)

if __name__=='__main__':
    print(answer("Which competitors are busiest around 6pm and what should I do?"))
