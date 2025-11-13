# src/embeddings_faiss.py
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

model = SentenceTransformer('all-MiniLM-L6-v2')

def build_vector_store():
    stores = pd.read_csv("data/stores.csv")
    peaks = pd.read_csv("data/store_peak_hours.csv")
    merged = stores.merge(peaks, on="store_id")
    docs = []
    meta=[]
    for _, r in merged.iterrows():
        txt = f"{r['name']}. Address: {r['address']}. Usual busiest hour: {int(r['peak_hour'])}. Typical peak footfall: {int(r['peak_count'])}."
        docs.append(txt)
        meta.append(dict(store_id=int(r['store_id']), name=r['name'], lat=r['lat'], lon=r['lon']))
    embeddings = model.encode(docs, convert_to_numpy=True)
    dim = embeddings.shape[1]
    idx = faiss.IndexFlatL2(dim)
    idx.add(embeddings)
    faiss.write_index(idx, "data/faiss_index.idx")
    with open("data/faiss_meta.pkl","wb") as f:
        pickle.dump({"docs":docs,"meta":meta,"embeddings":embeddings}, f)
    print("Saved faiss_index and meta")
if __name__=='__main__':
    build_vector_store()
