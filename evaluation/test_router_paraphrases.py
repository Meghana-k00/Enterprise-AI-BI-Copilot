
import pytest

from graph.router import QueryRouter


@pytest.mark.parametrize(
    ("question", "expected_route"),
    [
        ("Show me sales by region", "SQL"),
        ("Predict revenue for next month", "ANALYTICS"),
        ("Can I get my money back?", "RAG"),
    ],
)
def test_router_handles_paraphrased_questions(question, expected_route):
    router = QueryRouter()

    actual_route = router.route(question)

    assert actual_route == expected_route, (
        f"Question: {question!r}; "
        f"expected {expected_route}, got {actual_route}"
    )
