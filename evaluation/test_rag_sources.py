
import pytest

from rag.rag_engine import RAGEngine


@pytest.mark.parametrize(
    ("question", "expected_source"),
    [
        (
            "What is the maximum standard discount allowed?",
            "discount_policy.txt",
        ),
        (
            "What is the refund policy?",
            "refund_policy.txt",
        ),
        (
            "What customer policies are available?",
            "customer_policy.txt",
        ),
    ],
)
def test_rag_returns_expected_policy_source(question, expected_source):
    rag = RAGEngine()
    result = rag.answer(question)

    sources = [source.replace("\\", "/") for source in result["sources"]]

    assert any(expected_source in source for source in sources), (
        f"Question: {question!r}; "
        f"expected source {expected_source!r}; "
        f"got sources: {sources!r}"
    )
