
import pytest

from graph.router import QueryRouter


@pytest.mark.parametrize(
    ("question", "expected_route"),
    [
        ("What is the refund policy?", "RAG"),
        ("Can I get my money back?", "RAG"),
        ("What is the maximum standard discount allowed?", "RAG"),
        ("Are discounts above the standard limit permitted?", "RAG"),
    ],
)
def test_policy_question_routing(question, expected_route):
    router = QueryRouter()

    actual_route = router.route(question)

    assert actual_route == expected_route, (
        f"Question: {question!r}; "
        f"expected {expected_route}, got {actual_route}"
    )
