import os

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Multilingual Knowledge Assistant")

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://host.docker.internal:11434",
)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful multilingual assistant. "
                            "Answer clearly in the language of the "
                            "user's question."
                        ),
                    },
                    {
                        "role": "user",
                        "content": request.question,
                    },
                ],
                "stream": False,
            },
            timeout=180,
        )
        response.raise_for_status()
        result = response.json()

        return {
            "answer": result["message"]["content"],
            "model": OLLAMA_MODEL,
        }

    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "Could not reach Ollama. Check that Ollama is "
                "running on Windows and the model is available."
            ),
        ) from exc