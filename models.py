from datetime import datetime

from sqlalchemy import Identity, String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum
from schemas import TicketPriority, TicketStatus


class Base(DeclarativeBase):
    pass


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(
        Identity(always=True),
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    priority: Mapped[TicketPriority] = mapped_column(
        SQLEnum(
            TicketPriority,
            values_callable=lambda enum_class: [
                member.value for member in enum_class
            ],
            name="ticket_priority",
        ),
        nullable=False
    )

    status: Mapped[TicketStatus] = mapped_column(
        SQLEnum(
            TicketStatus,
            values_callable=lambda enum_class: [
                member.value for member in enum_class
            ],
            name="ticket_status",
        ),
        nullable=False,
        default=TicketStatus.OPEN
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )