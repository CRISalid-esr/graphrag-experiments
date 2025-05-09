"""
    This module defines the data models used in the application.
"""
from collections import defaultdict
from typing import List, Optional, Literal

from pydantic import BaseModel


class ChatMessage(BaseModel):
    """
    Represents a message in the chat history.
    """
    message: str
    type: Literal["user", "bot"]
    id: int
    loading: Optional[bool] = None


class ChatRequest(BaseModel):
    """
    Represents a request to the chat API.
    """
    history: List[ChatMessage]
    message: str
    metadata: dict = defaultdict(dict)


class ChatResponse(BaseModel):
    """
    Represents a response from the chat API.
    """
    reply: str
    query: Optional[str] = None
