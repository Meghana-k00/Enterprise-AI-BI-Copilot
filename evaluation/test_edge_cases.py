
import pytest
from graph.router import QueryRouter


@pytest.mark.parametrize(
    ("question", "expected_route"),
    [
        # SQL: structured business data
        ("Show me sales by region", "SQL"),
        ("How many customers do we have?", "SQL"),
        ("Which product generated the most revenue?", "SQL"),
        ("What is the total sales revenue?", "SQL"),

        # RAG: company policies and rules
        ("Can I get my money back?", "RAG"),
        ("What is the maximum standard discount allowed?", "RAG"),
        ("What is the refund policy?", "RAG"),

        # Analytics: statistical and forecasting questions
        ("Predict revenue for next month", "ANALYTICS"),
        ("Which month had the highest revenue?", "ANALYTICS"),
        ("What is the average order value?", "ANALYTICS"),
    ],
)
def test_edge_case_routing(question, expected_route):
    router = QueryRouter()

    actual_route = router.route(question)

    assert actual_route == expected_route, (
        f"Question: {question!r}; "
        f"expected {expected_route}, got {actual_route}"
    )
