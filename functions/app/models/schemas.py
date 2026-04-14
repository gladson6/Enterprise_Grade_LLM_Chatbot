from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    """
    Represents a single message in the chat history.
    'role' can be 'user' or 'assistant'.
    """
    role: str
    content: str

class ChatRequest(BaseModel):
    """
    Defines the structure of a request to the /chat endpoint.
    """
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    """
    Defines the structure of a response from the /chat endpoint.
    'sources' will list the document names from which the answer was derived.
    """
    reply: str
    sources: List[str]

class Lead(BaseModel):
    """
    Optional schema for a lead capture form.
    """
    name: str
    email: str
    company: Optional[str] = None
    query: str
