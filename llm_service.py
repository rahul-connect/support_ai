from groq import Groq
from conversation_models import Message
from config import settings
from groq.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
)

from schemas import MessageRole

from typing import Literal
from pydantic import BaseModel
from collections.abc import Iterator


class TicketClassification(BaseModel):
    category: Literal["delivery", "refund", "product", "other"]
    priority: Literal["low", "medium", "high"]
    order_id: str | None = None

client = Groq(api_key=settings.groq_api_key)

MAX_HISTORY_MESSAGES = 20


SYSTEM_PROMPT = """
    # Role
    You are a professional customer support assistant for an online store.

    # Task
    Help customers with:
    - Order inquiries
    - Delivery problems
    - Refund questions
    - Product issues

    # Rules
    - Be polite, clear, and concise.
    - Never invent order statuses, tracking numbers, or refund approvals.
    - If you don't have enough information, ask the customer for clarification.
    - Never claim that you checked an order unless actual order information was provided.
    - Keep responses under 100 words.

    # Examples

    Example 1:
    Customer: Where is my order ORDER-100?
    Assistant: I don't have access to live order-tracking information.
    Please check the tracking link in your confirmation email.

    Example 2:
    Customer: Has my refund been approved?
    Assistant: I can't verify refund approvals directly.
    Please check your refund confirmation email or contact the store's support team.
    """

def build_llm_messages(
    history: list[Message],
) -> list[ChatCompletionMessageParam]:


    system_message: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }

    llm_messages: list[ChatCompletionMessageParam] = [system_message]

    trimmed_history = trim_history(
        history,
        MAX_HISTORY_MESSAGES,
    )

    for message in trimmed_history:
        if message.role == MessageRole.USER:
            user_message: ChatCompletionUserMessageParam = {
                "role": "user",
                "content": message.content,
            }

            llm_messages.append(user_message)

        elif message.role == MessageRole.ASSISTANT:
            assistant_message: ChatCompletionAssistantMessageParam = {
                "role": "assistant",
                "content": message.content,
            }

            llm_messages.append(assistant_message)

    return llm_messages


def generate_reply(history: list[Message]) -> str:
    messages = build_llm_messages(history)

    completion = client.chat.completions.create(
        model=settings.model_name,
        messages=messages,
    )

    reply = completion.choices[0].message.content

    usage = completion.usage

    if usage is not None:
        print("Prompt tokens:", usage.prompt_tokens)
        print("Completion tokens:", usage.completion_tokens)
        print("Total tokens:", usage.total_tokens)
    else:
        print("Token usage information unavailable.")

    print("Finish reason:", completion.choices[0].finish_reason)

    if reply is None:
        raise ValueError("LLM returned no text response")

    return reply

def trim_history(
    messages: list[Message],
    max_messages: int,
) -> list[Message]:
    if len(messages) > max_messages:
        return messages[-max_messages:]
    return messages


def summarize_conversation(
    conversation_text: str,
) -> str:
    system_prompt = """
    You summarize customer support conversations.

    Preserve:
    - Order numbers and product names.
    - Problems reported by the customer.
    - Important troubleshooting steps.
    - Actions already taken.
    - Unresolved questions.

    Do not invent information.
    Keep the summary under 150 words.
    """

    completion = client.chat.completions.create(
    model=settings.model_name,
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": conversation_text,
        },
    ],
    )

    response = completion.choices[0].message.content

    usage = completion.usage

    if usage is not None:
        print("Prompt tokens:", usage.prompt_tokens)
        print("Completion tokens:", usage.completion_tokens)
        print("Total tokens:", usage.total_tokens)
    else:
        print("Token usage information unavailable.")

    print("Finish reason:", completion.choices[0].finish_reason)

    if response is None:
        raise ValueError("LLM returned no text response")

    return response



def classify_ticket(
    customer_message: str,
) -> TicketClassification:
    # Your implementation

    completion = client.chat.completions.create(
        model=settings.model_name,
        messages=[
            {
                "role": "system",
                "content": """
                Classify customer support messages.

                Return only a JSON object with:
                - category: delivery, refund, product, or other
                - priority: low, medium, or high
                - order_id: string or null

                Do not include markdown or explanations.
                """,
            },
            {
                "role": "user",
                "content": customer_message,
            },
        ],
        response_format={"type": "json_object"},
    )


    response = completion.choices[0].message.content

    usage = completion.usage

    if usage is not None:
        print("Prompt tokens:", usage.prompt_tokens)
        print("Completion tokens:", usage.completion_tokens)
        print("Total tokens:", usage.total_tokens)
    else:
        print("Token usage information unavailable.")

    print("Finish reason:", completion.choices[0].finish_reason)

    if response is None:
        raise ValueError("LLM returned no text response")

    return TicketClassification.model_validate_json(response)


def stream_reply(
    history: list[Message],
) -> Iterator[str]:
    stream = client.chat.completions.create(
        model=settings.model_name,
        messages=build_llm_messages(history),
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content

        if content is not None:
            yield content


def get_order_status(order_id: str) -> dict:
    orders = {
        "ORDER-123": {
            "status": "shipped",
            "estimated_delivery": "2026-10-20",
        },
        "ORDER-456": {
            "status": "delivered",
            "estimated_delivery": "2026-10-15",
        },
    }

    return orders.get(
        order_id,
        {"error": "Order not found"},
    )