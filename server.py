from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key="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")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "AI server running 🚀"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": req.message}],
            max_tokens=1024
        )
        reply = completion.choices[0].message.content
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"Ошибка: {str(e)}"}
