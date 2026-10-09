
import pytest

from rag.rag_engine import RAGEngine


@pytest.mark.parametrize(
    ("question", "expected_keywords"),
    [
        (
            "What is the maximum standard discount allowed?",
            ["10%"],
        ),
        (
            "What is the refund policy?",
            ["refund"],
        ),
    ],
)
def test_rag_answer_contains_expected_information(
    question, expected_keywords
):
    rag = RAGEngine()
    result = rag.answer(question)

    answer = result["answer"].lower()

    for keyword in expected_keywords:
        assert keyword.lower() in answer, (
            f"Question: {question!r}; "
            f"expected {keyword!r} in answer, "
            f"got: {result['answer']!r}"
        )

    assert result["sources"], (
        f"No sources returned for question: {question!r}"
    )
