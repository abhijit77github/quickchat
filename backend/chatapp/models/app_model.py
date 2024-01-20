
from pydantic import BaseModel, Field
from enum import Enum

class MessageStatus(str, Enum):
    """doc string"""
    sent = "sent"
    delivered = "delivered"
    read = "read"
    
class EventType(str, Enum):
    """doc string"""
    message = "message"
    chat_history = "chat_history"
    user_status = "user_status"
    

class Message(BaseModel):
    """doc string"""
    msg_id: str = Field(..., min_length=1, max_length=10)
    message: str = Field(..., min_length=1, max_length=100)
    sender_id: str = Field(..., min_length=1, max_length=10)
    receiver_id: str = Field(..., min_length=1, max_length=10)
    timestamp: str = Field(..., min_length=1, max_length=20)
    delivered_at: str = Field(..., min_length=1, max_length=20)
    read_at: str = Field(..., min_length=1, max_length=20)
    status: MessageStatus
    
    
    class Config:
        """doc string"""
        schema_extra = {
            "example": {
                "message": "Hello World",
                "sender_id": "user1",
            }
        }
        
class EventMessage(BaseModel):
    event_type: EventType
    event_msg: dict