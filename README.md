# Banking Support Chatbot 🏦🤖

An AI-powered banking assistant that uses RAG (Retrieval-Augmented Generation) to answer banking queries accurately based on uploaded documents.

🚀 **Live Deployment:** [Click here to use the Chatbot!](https://banking-chatbot-frontend-lyk3.onrender.com)

> ⚠️ **Note on Performance:** This project is hosted on Render's free tier. If the chatbot is inactive for 15 minutes, the server will go to "sleep" to save power. When you send the very first message after a period of inactivity, it might take about 50 seconds to get a reply while the server wakes up. After that, it will be super fast!


## Architecture
- **Frontend:** React + Vite
- **Backend:** FastAPI (Python)
- **AI Model:** Google Gemini (Generative AI)
- **Vector Database:** Chroma DB
- **Embeddings:** SentenceTransformers (all-MiniLM-L6-v2)

## Features
- **Intelligent Q&A:** Retrieves context from uploaded PDFs to ground the AI's answers.
- **FastAPI Backend:** High-performance, async backend handling AI tasks.
- **Modern UI:** Clean, responsive React interface.

---
*Deployed via Render*
