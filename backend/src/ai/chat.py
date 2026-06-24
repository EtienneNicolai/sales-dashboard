from anthropic import Anthropic
from backend.src.data.models import SalesRow
import os

client = None


def build_context(rows: list[SalesRow]) -> str:
    lines = ["date,product,category,quantity,unit_price,revenue,region"]
    for r in rows:
        lines.append(f"{r.date},{r.product},{r.category},{r.quantity},{r.unit_price},{r.revenue},{r.region}")
    return "\n".join(lines)


def ask(rows: list[SalesRow], question: str) -> str:
    global client
    if client is None:
        client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    context = build_context(rows)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "You are a data analyst. Below is a sales dataset in CSV format.\n\n"
                    f"{context}\n\n"
                    f"Question: {question}\n\n"
                    "Answer concisely using only the data above. Do not invent figures."
                ),
            }
        ],
    )
    return message.content[0].text
