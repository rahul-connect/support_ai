from schemas import TicketResponse, TicketCreate
from exceptions import TicketNotFoundError
from sqlalchemy.orm import Session
from repository import PostgresTicketRepository

class TicketService:
    def __init__(self, db: Session, ticket_repository: PostgresTicketRepository):
        self.db = db
        self.ticket_repository = ticket_repository

    def create_ticket(self, ticket_data: TicketCreate) -> TicketResponse:
        try:
            ticket = self.ticket_repository.create(ticket_data)

            response = TicketResponse.model_validate(ticket)

            self.db.commit()

            return response

        except Exception:
            self.db.rollback()
            raise



    def get_ticket(self, ticket_id: int) -> TicketResponse:
        ticket = self.ticket_repository.get_by_id(ticket_id)

        if ticket is None:
            raise TicketNotFoundError(ticket_id)

        return TicketResponse.model_validate(ticket)




