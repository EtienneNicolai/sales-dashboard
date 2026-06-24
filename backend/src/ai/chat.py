import google.generativeai as genai
import os
from backend.src.data.models import SalesRow

model = None


def build_context(rows: list[SalesRow]) -> str:
    lines = ["date,product,category,quantity,unit_price,revenue,region"]
    for r in rows:
        lines.append(f"{r.date},{r.product},{r.category},{r.quantity},{r.unit_price},{r.revenue},{r.region}")
    return "\n".join(lines)


def ask(rows: list[SalesRow], question: str) -> str:
    global model
    if model is None:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
    context = build_context(rows)
    prompt = (
        "You are a data analyst. Below is a sales dataset in CSV format.\n\n"
        f"{context}\n\n"
        f"Question: {question}\n\n"
        "Answer concisely using only the data above. Do not invent figures."
    )
    response = model.generate_content(prompt)
    return response.text
