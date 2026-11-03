from sqlalchemy.orm import Session
from sqlalchemy import select

from conversation_models import Conversation, Message
from schemas import MessageRole


class PostgresConversationRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_messages(self, conversation_id) -> list[Message]:

        stmt = (select(Message)
                .where(Message.conversation_id==conversation_id)
                .order_by(Message.created_at.asc(), Message.id.asc())
                )

        messages = list(self.db.scalars(stmt).all())

        return messages

    def get_recent_messages(
        self,
        conversation_id: int,
        limit: int,
    ) -> list[Message]:
        
        stmt = (select(Message)
                .where(Message.conversation_id==conversation_id)
                .order_by(Message.created_at.desc(), Message.id.desc())
                .limit(limit)
                )

        messages = list(self.db.scalars(stmt).all())

        messages.reverse()

        return messages

    def get_conversation(self, conversation_id: int) -> Conversation | None:
        
        stmt = select(Conversation).where(Conversation.id == conversation_id)

        return self.db.scalar(stmt)

    def create_conversation(self, title: str | None = None) -> Conversation:
        conversation = Conversation(title=title)

        self.db.add(conversation)
        self.db.flush()
        return conversation

    def create_message(
            self,
            conversation_id: int,
            role:MessageRole,
            content: str,
        ) -> Message:
        
        message = Message(
            conversation_id = conversation_id,
            role = role,
            content = content
        )

        self.db.add(message)
        self.db.flush()
        return message

