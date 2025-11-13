from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Model(BaseModel):
    id: str
    object: str = "model"
    created: int
    owned_by: str

class ModelListResponse(BaseModel):
    data: List[Model]
    object: str = "list"

class OpenAIMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[OpenAIMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 512

class ChatCompletionResponse(BaseModel):
    id: str = "oumi-response-123"
    object: str = "chat.completion"
    created: int = 1629263152
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int] = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}