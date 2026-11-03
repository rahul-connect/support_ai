from schemas import TicketCreate, TicketResponse, TicketStatus
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Ticket

class TicketRepository:
    def __init__(self):
        self.tickets = {}
        self.next_id = 1

    def create(self, ticket_data: TicketCreate) -> TicketResponse:
        created_ticket = TicketResponse(
            id= self.next_id,
            title=ticket_data.title,
            description=ticket_data.description,
            priority=ticket_data.priority,
            status=TicketStatus.OPEN
        )

        self.tickets[created_ticket.id] = created_ticket

        self.next_id += 1

        return created_ticket


    def get_by_id(self, ticket_id: int) -> TicketResponse | None:
        return self.tickets.get(ticket_id)


class PostgresTicketRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, ticket_id: int) -> Ticket | None:
      stmt = select(Ticket).where(Ticket.id==ticket_id)
      return self.db.scalars(stmt).first()


    def create(self, ticket_data: TicketCreate) -> Ticket:
        ticket = Ticket(
            title=ticket_data.title,
            description=ticket_data.description,
            priority=ticket_data.priority,
        )
        self.db.add(ticket)
        self.db.flush()
        self.db.refresh(ticket)
        return ticket