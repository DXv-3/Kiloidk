"""Pydantic models for the AI agent application."""
from typing import Any
from pydantic import BaseModel


class ToolCall(BaseModel):
    name: str
    input: dict[str, Any]
    output: dict[str, Any]
    duration: float = 0.0


class AgentResponse(BaseModel):
    text: str
    tool_calls: list[ToolCall] = []
    entities_extracted: list[dict] = []
    preferences_detected: list[dict] = []
