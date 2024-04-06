from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import agents.api.schemas
import agents.crud
from agents.database import SessionLocal, engine
from agents.processing import (craft_agent_chat_context,
                               craft_agent_chat_first_message,
                               craft_agent_chat_instructions)
from agentsfwrk import integrations, logger

log = logger.get_logger(__name__)

router = APIRouter(
    prefix="/agents",
    tags=["Chat"],
    responses={404: {"description": "Not found"}}
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/chat-agent", response_model=agents.api.schemas.ChatAgentResponse)
async def chat_completion(message: agents.api.schemas.UserMessage, db: Session = Depends(get_db)):
    log.info(f"User conversation id: {message.conversation_id}")
    log.info(f"User message: {message.message}")

    conversation = agents.crud.get_conversation(db, message.conversation_id)

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found. Please create the conversation first."
        )

    log.info(f"Conversation id: {conversation.id}")

    context = craft_agent_chat_context(conversation.agent.context)
    chat_messages = [craft_agent_chat_first_message(conversation.agent.first_message)]

    # Sorting and appending historical messages
    hist_messages = sorted(conversation.messages, key=lambda x: x.timestamp)
    for mes in hist_messages:
        log.info(f"Conversation history message: {mes.user_message} | {mes.agent_message}")
        chat_messages.extend([
            {"role": "user", "content": mes.user_message},
            {"role": "assistant", "content": mes.agent_message}
        ])

    service = integrations.OpenAIIntegrationService(context, craft_agent_chat_instructions(conversation.agent.instructions, conversation.agent.response_shape))
    service.add_chat_history(chat_messages)

    response = service.answer_to_prompt(
        model="gpt-3.5-turbo",
        prompt=message.message,
        temperature=0.5,
        max_tokens=1000,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    log.info(f"Agent response: {response['answer']}")

    # Save interaction to database
    db_message = agents.crud.create_conversation_message(
        db, conversation.id, 
        agents.api.schemas.MessageCreate(user_message=message.message, agent_message=response['answer'])
    )
    log.info(f"Conversation message id {db_message.id} saved to database")

    return agents.api.schemas.ChatAgentResponse(
        conversation_id=message.conversation_id,
        response=response['answer']
    )
