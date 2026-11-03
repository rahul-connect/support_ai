from conversation_models import Message
from llm_service import generate_reply
from schemas import MessageRole


history = [
    Message(
        role=MessageRole.USER,
        content="What is Python? Answer in one sentence.",
    )
]

reply = generate_reply(history)

print("AI Response:", reply)