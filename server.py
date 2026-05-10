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
            GEMINI_URL,
            json={
                "contents": [
                    {"parts": [{"text": req.message}]}
                ]
            },
            timeout=30
        )
        data = response.json()
        if "candidates" in data:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in data:
            reply = f"Gemini ошибка: {data['error']['message']}"
        else:
            reply = f"Неожиданный ответ: {str(data)}"
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"Ошибка: {str(e)}"}
