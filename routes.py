from fastapi import APIRouter, status
from schemas import TicketCreate, TicketResponse
from dependencies import TicketServiceDep

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket_data:TicketCreate,
    ticket_service:TicketServiceDep
    ) -> TicketResponse:
    return ticket_service.create_ticket(ticket_data)


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK
)
def get_ticket(
    ticket_id:int,
    ticket_service:TicketServiceDep
    ) -> TicketResponse:
    return ticket_service.get_ticket(ticket_id)