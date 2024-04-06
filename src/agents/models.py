from sqlalchemy import Column, ForeignKey, String, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from agents.database import Base

class Agent(Base):
    __tablename__ = "agents"

    id          = Column(String, primary_key = True, index = True)
    timestamp   = Column(DateTimefrom sqlalchemy import Column, ForeignKey, String, DateTime, JSON, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID  # Importing UUID for a more robust ID handling

from agents.database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    timestamp = Column(DateTime, default=func.now, nullable=False)

    context = Column(String, nullable=False)
    first_message = Column(String, nullable=False)
    response_shape = Column(JSON, nullable=False)
    instructions = Column(String, nullable=False)

    conversations = relationship("Conversation", back_populates="agent")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"))
    timestamp = Column(DateTime, default=func.now, nullable=False)

    agent = relationship("Agent", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    timestamp = Column(DateTime, default=func.now, nullable=False)

    user_message = Column(String, nullable=False)
    agent_message = Column(String, nullable=False)

    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"))
    conversation = relationship("Conversation", back_populates="messages")
, default = datetime.utcnow)

    context            = Column(String, nullable = False)
    first_message      = Column(String, nullable = False)
    response_shape     = Column(JSON,   nullable = False)
    instructions       = Column(String, nullable = False)

    conversations      = relationship("Conversation", back_populates = "agent")


class Conversation(Base):
    __tablename__ = "conversations"

    id          = Column(String, primary_key = True, index = True)
    agent_id    = Column(String, ForeignKey("agents.id"))
    timestap    = Column(DateTime, default = datetime.utcnow)

    agent       = relationship("Agent", back_populates = "conversations")
    messages    = relationship("Message", back_populates = "conversation")


class Message(Base):
    __tablename__ = "messages"

    id          = Column(String, primary_key = True, index = True)
    timestamp   = Column(DateTime, default = datetime.utcnow)

    user_message    = Column(String)
    agent_message   = Column(String)

    conversation_id = Column(String, ForeignKey("conversations.id"))
    conversation    = relationship("Conversation", back_populates = "messages")
