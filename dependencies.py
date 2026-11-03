from typing import Annotated
from fastapi import Depends

from repository import PostgresTicketRepository
from service import TicketService
from sqlalchemy.orm import Session
from database import get_db
from conversation_repository import PostgresConversationRepository
from conversation_service import ConversationService

DbSession = Annotated[
    Session,
    Depends(get_db)
]


def get_ticket_service(db: DbSession) -> TicketService:
    ticket_repository = PostgresTicketRepository(db)

    ticket_service = TicketService(
        db=db,
        ticket_repository=ticket_repository,
    )

    return ticket_service


TicketServiceDep = Annotated[
    TicketService,
    Depends(get_ticket_service)
]


def get_conversation_service(
    db: DbSession,
) -> ConversationService:

    conversation_repository = PostgresConversationRepository(db)

    conversation_service = ConversationService(
        db=db,
        repository=conversation_repository,
    )

    return conversation_service


ConversationServiceDep = Annotated[
    ConversationService,
    Depends(get_conversation_service),
]