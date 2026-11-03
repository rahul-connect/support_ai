from datetime import datetime
from sqlalchemy import (
    Identity,
    String,
    Text,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import Base
from sqlalchemy import Enum as SQLEnum
from schemas import MessageRole


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        Identity(always=True),
        primary_key=True
        )
    title: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
        )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
        )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete",
        passive_deletes=True
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Identity(always=True),
        primary_key=True
    )
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey(
            "conversations.id",
            ondelete="CASCADE"
        ),
        nullable=False,
    )
    role: Mapped[MessageRole] = mapped_column(
        SQLEnum(
            MessageRole,
            values_callable=lambda enum_class: [
                member.value for member in enum_class
            ],
            name="message_role"
        ),
        nullable=False
    )
    content: Mapped[str] = mapped_column(
        Text(),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages",
    )