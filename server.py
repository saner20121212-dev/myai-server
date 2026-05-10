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

GEMINI_API_KEY = "AIzaSyD3pnJRqivlkchRTedsFcL2EcZ6xDXlJ7g"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

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
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"Ошибка: {str(e)}"}
