from unittest.mock import MagicMock, patch
from backend.src.data.models import SalesRow
from backend.src.ai.chat import build_context, ask

SAMPLE_ROWS = [
    SalesRow("2024-01-15", "Widget A", "Electronics", 10, 29.99, 299.90, "North"),
    SalesRow("2024-02-10", "Gadget B", "Electronics", 5, 49.99, 249.95, "South"),
]


def test_build_context_is_valid_csv():
    context = build_context(SAMPLE_ROWS)
    lines = context.strip().split("\n")
    assert lines[0] == "date,product,category,quantity,unit_price,revenue,region"
    assert len(lines) == len(SAMPLE_ROWS) + 1


def test_build_context_contains_product_names():
    context = build_context(SAMPLE_ROWS)
    assert "Widget A" in context
    assert "Gadget B" in context


def test_ask_calls_gemini_once():
    mock_response = MagicMock()
    mock_response.text = "Widget A had the highest revenue."
    with patch("backend.src.ai.chat.model") as mock_model:
        mock_model.generate_content.return_value = mock_response
        answer = ask(SAMPLE_ROWS, "Which product had the highest revenue?")
    mock_model.generate_content.assert_called_once()
    assert answer == "Widget A had the highest revenue."


def test_ask_includes_question_in_prompt():
    mock_response = MagicMock()
    mock_response.text = "Answer"
    with patch("backend.src.ai.chat.model") as mock_model:
        mock_model.generate_content.return_value = mock_response
        ask(SAMPLE_ROWS, "What is the best region?")
    prompt = mock_model.generate_content.call_args.args[0]
    assert "What is the best region?" in prompt
