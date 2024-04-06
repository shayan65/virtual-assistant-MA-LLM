from datetime import datetime
from typing import List
from pydantic import BaseModel


class ConversationBase(BaseModel):
    agent_id: str


class Conversation(ConversationBase):
    id: str
    timestamp: datetime  # No default value here; let the ORM handle it

    class Config:
        orm_mode = True


class AgentBase(BaseModel):
    context: str
    first_message: str
    response_shape: str
    instructions: str


class Agent(AgentBase):
    id: str
    timestamp: datetime  # No default value here; let the ORM handle it
    conversations: List[Conversation] = []

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    user_message: str
    agent_message: str


class Message(MessageBase):
    id: str
    timestamp: datetime  # No default value here; let the ORM handle it
    conversation_id: str

    class Config:
        orm_mode = True


class UserMessage(BaseModel):
    conversation_id: str
    message: str


class ChatAgentResponse(BaseModel):
    conversation_id: str
    response: str
