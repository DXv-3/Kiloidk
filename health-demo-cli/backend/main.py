"""FastAPI backend for AI agent application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json

app = FastAPI(title="AI Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    history: list = []


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "neo4j": "stubbed"}


@app.post("/chat")
async def chat(request: ChatRequest):
    """Chat endpoint."""
    return {"text": f"Response to: {request.message}", "tool_calls": [], "entities_extracted": [], "preferences_detected": []}


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint."""
    async def generate():
        data = {"type": "text_delta", "content": "Hello"}
        yield f"data: {json.dumps(data)}\n\n"
        data = {"type": "done"}
        yield f"data: {json.dumps(data)}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/schema/visualization")
async def schema_visualization():
    """Graph schema for visualization."""
    return {
        "nodes": [{"id": "Patient", "label": "Patient", "color": "#4CAF50"}],
        "edges": []
    }
