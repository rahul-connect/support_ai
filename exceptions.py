from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class TicketNotFoundError(Exception):
    def __init__(self, ticket_id: int):
        self.ticket_id = ticket_id
        super().__init__(f"Ticket {ticket_id} not found")


class ConversationNotFoundError(Exception):
    def __init__(self, conversation_id: int):
        self.conversation_id = conversation_id
        super().__init__(f"Conversation {conversation_id} not found")



def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(TicketNotFoundError)
    async def ticket_not_found_handler(
        request: Request,
        exc: TicketNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)}
        )

    @app.exception_handler(ConversationNotFoundError)
    async def conversation_not_found_handler(
        request: Request,
        exc: ConversationNotFoundError
    )-> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)}
        )



