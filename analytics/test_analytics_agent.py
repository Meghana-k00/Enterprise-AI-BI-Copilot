import numbers

from analytics_agent import AnalyticsAgent


def test_analytics_agent_forecast():
    agent = AnalyticsAgent()

    question = "What is the forecast for next month's revenue?"

    result = agent.run(question)

    assert result is not None

    if isinstance(result, dict):
        assert "answer" in result
        assert result["answer"] is not None
        assert str(result["answer"]).strip() != ""
    else:
        assert isinstance(result, str)
        assert result.strip() != ""