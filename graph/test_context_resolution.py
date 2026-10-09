
from unittest.mock import patch, Mock
from types import SimpleNamespace

from graph.supervisor import resolve_context




def test_follow_up_question_uses_previous_context():
    messages = [
        {
            "role": "user",
            "content": "What is the total sales revenue by region?",
        },
        {
            "role": "assistant",
            "content": "North has the highest revenue.",
        },
    ]

    expected_question = "Which region has the highest sales revenue?"

    with patch(
        "graph.supervisor.resolve_context",
        return_value=expected_question,
    ) as mock_resolve:
        result = mock_resolve("What about it?", messages)

    assert result == expected_question
    mock_resolve.assert_called_once_with("What about it?", messages)



def test_standalone_question_does_not_call_context_llm():
    question = "What is the refund policy?"

    messages = [
        {"role": "user", "content": "What is the total revenue?"}
    ]

    with patch("graph.supervisor.context_llm") as mock_llm:
        result = resolve_context(question, messages)

    assert result == question
    mock_llm.invoke.assert_not_called()


def test_question_without_history_is_returned_unchanged():
    question = "What is the refund policy?"

    assert resolve_context(question, []) == question


def test_follow_up_preserves_second_highest_intent():
    messages = [
        {
            "role": "user",
            "content": "Which region has the highest sales revenue?",
        },
        {
            "role": "assistant",
            "content": "North has the highest sales revenue.",
        },
    ]

    result = resolve_context("What about the second highest?", messages)
    print(f"\nResolved follow-up: {result}")

    assert result.strip()
    assert "region" in result.lower()
    assert "revenue" in result.lower()
    assert "second" in result.lower()
