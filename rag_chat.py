import chromadb # type: ignore
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import requests

# === Setup ===
chroma_dir = "./kb"
model_name = "BAAI/bge-small-en"
GROQ_API_KEY = "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"
GROQ_MODEL= "llama3-8b-8192"  # or llama3-70b-8192 depending on your access

# === Embedding ===
def get_embed_fun():
    model_kwargs = {"device": "cuda"}
    encode_kwargs = {"normalize_embeddings": True}
    return HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
db = Chroma(persist_directory=chroma_dir, embedding_function=get_embed_fun())

# === Chroma Vector Store ===
def load_chroma():
    return Chroma(persist_directory=chroma_dir, embedding_function=get_embed_fun())

# === Query Vector DB ===
def get_context(query: str, k: int = 3):
    docs = db.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])

# === Groq API ===
def call_groq_api(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# === Full RAG Pipeline ===
def answer_query(query: str):
    context = get_context(query)
    #print(context)
    prompt = f"""You are an AI assistant helping customers with insurance questions.
Use the following context from our knowledge base to answer clearly and accurately when needed.
Generalize the answer and don't mention about the context in your answer to the user.
Context:
{context}

Question: {query}
Answer:"""
    return call_groq_api(prompt)

# === Demo Usage ===
if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or type 'exit'): ")
        if q.lower() == "exit":
            break
        print("\nAnswer:", answer_query(q))
