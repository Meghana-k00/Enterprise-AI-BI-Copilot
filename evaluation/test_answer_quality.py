
import pytest

from analytics.analytics_engine import AnalyticsEngine
from analytics.forecasting import RevenueForecaster
from rag.rag_engine import RAGEngine


@pytest.mark.parametrize(
    ("question", "expected_keywords"),
    [
        (
            "What is the refund policy?",
            ["refund", "order"],
        ),
        (
            "What is the maximum standard discount allowed?",
            ["10%"],
        ),
    ],
)
def test_policy_answers_contain_expected_information(
    question, expected_keywords
):
    rag = RAGEngine()
    result = rag.answer(question)

    answer = result["answer"].casefold()

    for keyword in expected_keywords:
        assert keyword.casefold() in answer, (
            f"Missing {keyword!r} in answer: {result['answer']!r}"
        )

    assert result["sources"], "Expected policy sources to be returned"


def test_total_revenue_matches_sales_data():
    engine = AnalyticsEngine()

    actual = engine.total_revenue()

    assert actual == pytest.approx(16370.00)


def test_revenue_forecast_is_a_valid_positive_number():
    forecaster = RevenueForecaster()

    forecast = forecaster.forecast_next_month()

    assert isinstance(forecast, (int, float))
    assert forecast > 0
