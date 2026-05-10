from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "AI server running 🚀"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": req.message,
                "stream": False
            },
            headers={"ngrok-skip-browser-warning": "true"},
            timeout=120
        )
        data = response.json()
        return {"reply": data.get("response", "No response")}
    except Exception as e:
        return {"reply": f"Ошибка сервера: {str(e)}"}