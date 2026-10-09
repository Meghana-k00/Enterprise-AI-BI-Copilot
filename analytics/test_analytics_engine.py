import numbers
import pandas as pd

from analytics_engine import AnalyticsEngine


def test_total_revenue():
    analytics = AnalyticsEngine()

    result = analytics.total_revenue()

    assert isinstance(result, numbers.Number)
    assert result == 16370


def test_revenue_by_region():
    analytics = AnalyticsEngine()

    result = analytics.revenue_by_region()

    assert isinstance(result, pd.Series)
    assert not result.empty
    assert result.sum() == analytics.total_revenue()


def test_monthly_revenue():
    analytics = AnalyticsEngine()

    result = analytics.monthly_revenue()

    assert isinstance(result, pd.Series)
    assert not result.empty
    assert result.sum() == analytics.total_revenue()


def test_average_order_value():
    analytics = AnalyticsEngine()

    result = analytics.average_order_value()

    assert isinstance(result, numbers.Number)
    assert result > 0