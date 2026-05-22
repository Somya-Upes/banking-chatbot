from sentence_transformers import SentenceTransformer
import chromadb
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Create ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create collection
collection = chroma_client.get_or_create_collection(name="banking_docs")

# Load Gemini API key
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

gemini_model = genai.GenerativeModel("models/gemini-2.5-flash")

def store_chunks(chunks):
    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()

        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk]
        )

    print(f"Stored {len(chunks)} chunks in ChromaDB")


def search_chunks(query, top_k=3):
    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]


def generate_answer(query):
    relevant_chunks = search_chunks(query)

    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are a helpful banking support chatbot.

Answer the user's question using ONLY the context below.

If the answer is not available in the context, say:
"I don't have enough information in the uploaded documents."

Context:
{context}

User question:
{query}

Answer:
"""

    try:
        response = gemini_model.generate_content(prompt)
        return response.text, relevant_chunks

    except Exception as e:
        print("\nGemini API Error:\n")
        print(e)
        return "Gemini API failed. Please check quota or API key.", relevant_chunks


if __name__ == "__main__":
    question = "What is pension?"

    answer, sources = generate_answer(question)

    print("\nAI Answer:\n")
    print(answer)

    print("\nSources Used:\n")
    for source in sources:
        print(source[:300])
        print("-----")