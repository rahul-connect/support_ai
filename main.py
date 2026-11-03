from fastapi import FastAPI
from routes import router as ticket_router
from conversation_routes import router as conversation_router
from exceptions import register_exception_handlers

app = FastAPI()


app.include_router(ticket_router)
app.include_router(conversation_router)

register_exception_handlers(app)