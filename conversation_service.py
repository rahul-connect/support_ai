from sqlalchemy.orm import Session

from conversation_repository import PostgresConversationRepository
from conversation_models import Conversation, Message
from schemas import MessageRole
from exceptions import ConversationNotFoundError
from llm_service import generate_reply



class ConversationService:

    def __init__(
            self,
            repository: PostgresConversationRepository,
            db: Session,
    ):
        self.repository = repository
        self.db = db

    def start_conversation(
        self,
        title: str | None,
        first_message: str,
    ) -> Conversation:

        try:
            conversation = self.repository.create_conversation(title=title)

            self.repository.create_message(
                conversation_id=conversation.id,
                role=MessageRole.USER,
                content=first_message,
            )

            self.db.commit()
            return conversation

        except Exception:
            self.db.rollback()
            raise

    def add_message(
        self,
        conversation_id: int,
        role: MessageRole,
        content: str,
    ) -> Message:

        try:
            conversation = self.repository.get_conversation(
                conversation_id=conversation_id
            )

            if conversation is None:
                raise ConversationNotFoundError(conversation_id)

            message = self.repository.create_message(
                conversation_id=conversation.id,
                role=role,
                content=content,
            )

            self.db.commit()
            return message

        except Exception:
            self.db.rollback()
            raise


    def get_conversation_history(
        self,
        conversation_id: int,
    ) -> list[Message]:

        conversation = self.repository.get_conversation(
            conversation_id=conversation_id
        )

        if conversation is None:
            raise ConversationNotFoundError(conversation_id)

        messages = self.repository.get_messages(
            conversation_id=conversation.id
        )

        return messages


    def generate_ai_response(
        self,
        conversation_id: int,
    ) -> Message:

        history = self.repository.get_recent_messages(
            conversation_id=conversation_id,
            limit=20
        )

        ai_reply = generate_reply(history)

        assistant_message = self.add_message(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=ai_reply,
        )

        return assistant_message




    def chat(
        self,
        conversation_id: int,
        user_message: str,
    ) -> Message:

        self.add_message(
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=user_message,
        )

        assistant_message = self.generate_ai_response(
            conversation_id=conversation_id
        )

        return assistant_message



def update_customer_context(
    context: dict[str, str],
    new_facts: dict[str, str],
) -> dict[str, str]:

    updated_context = context.copy()

    updated_context.update(new_facts)

    return updated_context

