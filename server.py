from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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
        def generate():
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": req.message}],
                max_tokens=1024,
                stream=True
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta.encode("utf-8")

        return StreamingResponse(
            generate(),
            media_type="text/plain; charset=utf-8",
            headers={
                "X-Accel-Buffering": "no",
                "Cache-Control": "no-cache",
                "Transfer-Encoding": "chunked"
            }
        )
    except Exception as e:
        return {"reply": f"Ошибка: {str(e)}"}
