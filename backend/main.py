from backend.rag import generate_answer
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil

app = FastAPI(title="Banking Support Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []

chat_sessions = {}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Banking chatbot is running!"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    history = chat_sessions.get(request.session_id, [])
    history.append({"role": "user", "content": request.message})

    answer, sources = generate_answer(request.message)
    history.append({"role": "assistant", "content": answer})
    chat_sessions[request.session_id] = history

    return ChatResponse(answer=answer, sources=sources)
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    allowed_types = ["application/pdf", "text/plain"]

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")

    os.makedirs("data", exist_ok=True)
    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"File '{file.filename}' uploaded successfully!", "path": file_path}