
from fastapi import APIRouter, status

from dependencies import ConversationServiceDep
from schemas import ConversationCreate, ConversationResponse, MessageCreate, MessageResponse, MessageRole
from fastapi import HTTPException

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)

@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    payload: ConversationCreate,
    service: ConversationServiceDep,
):
    return service.start_conversation(
        title=payload.title,
        first_message=payload.first_message,
    )


@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def get_conversation_messages(
    conversation_id: int,
    service: ConversationServiceDep,
):
    return service.get_conversation_history(conversation_id)


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    conversation_id: int,
    payload: MessageCreate,
    service: ConversationServiceDep,
):
    return service.add_message(
        conversation_id=conversation_id,
        content=payload.content,
        role=MessageRole.USER
        )


@router.post(
    "/{conversation_id}/generate",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_conversation_reply(
    conversation_id: int,
    service: ConversationServiceDep,
):
    assistant_message = service.generate_ai_response(
        conversation_id=conversation_id
    )

    return assistant_message


@router.post(
    "/{conversation_id}/chat",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def chat_with_ai(
    conversation_id: int,
    payload: MessageCreate,
    service: ConversationServiceDep,
):
    assistant_message = service.chat(
        conversation_id=conversation_id,
        user_message=payload.content,
    )

    return assistant_message