from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime

class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=1000)
    priority: TicketPriority 


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: TicketPriority
    status: TicketStatus

    model_config = ConfigDict(from_attributes=True)


class MessageRole(str,Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ConversationCreate(BaseModel):
    title: str | None = Field(default=None, max_length=150)
    first_message: str = Field(min_length=1)


class ConversationResponse(BaseModel):
    id: int
    title: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: MessageRole
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageCreate(BaseModel):
    content: str = Field(min_length=1)