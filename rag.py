import faiss, numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from openai import APIConnectionError, OpenAI

emb = SentenceTransformer("all-MiniLM-L6-v2")
client = OpenAI(
    base_url="http://127.0.0.1:11434/v1",
    api_key="ollama",
    timeout=300.0,
)
chunks, index = [], None

def load_pdf(path, size=800, overlap=100):
    global chunks, index
    text = " ".join(p.extract_text() or "" for p in PdfReader(path).pages)
    chunks = [text[i:i+size] for i in range(0, len(text), size - overlap)]
    vecs = emb.encode(chunks, normalize_embeddings=True).astype("float32")
    index = faiss.IndexFlatIP(vecs.shape[1])
    index.add(vecs)

def ask(q, k=4):
    qv = emb.encode([q], normalize_embeddings=True).astype("float32")
    _, ids = index.search(qv, k)
    context = "\n---\n".join(chunks[i] for i in ids[0])
    try:
        r = client.chat.completions.create(
            model="llama3.2:3b",
            messages=[
                {"role": "system", "content": "Answer ONLY from the context. If not found, say you don't know."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {q}"},
            ],
        )
    except APIConnectionError as exc:
        raise RuntimeError(
            "Could not connect to Ollama. Make sure Ollama is running locally."
        ) from exc
    return r.choices[0].message.content