from langchain_ollama import ChatOllama

from analytics.analytics_engine import AnalyticsEngine
from analytics.forecasting import RevenueForecaster


class AnalyticsAgent:

    def __init__(self):

        self.analytics = AnalyticsEngine()

        self.forecaster = RevenueForecaster()

        self.llm = ChatOllama(
            model="qwen2.5:3b",
            temperature=0
        )

    # =====================================================
    # OPERATION CLASSIFICATION
    # =====================================================

    def classify_operation(self, question):

        prompt = f"""
You are an analytics operation classifier.

Identify the analytical operation requested by the user.

Return EXACTLY ONE:

AVERAGE_ORDER_VALUE
STANDARD_DEVIATION
HIGHEST_REVENUE_MONTH
LOWEST_REVENUE_MONTH
FORECAST_REVENUE

====================================================
AVERAGE_ORDER_VALUE
====================================================

Questions asking for average order amount/value.

Examples:

What is the average order value?
What is the average amount per order?
How much does an average order generate?

====================================================
STANDARD_DEVIATION
====================================================

Questions asking about variability, spread,
dispersion or standard deviation of sales.

Examples:

How much do our sales vary?
How much do our sales differ?
How spread out are sales?
How inconsistent are sales?
What is the standard deviation?
What is the variability of sales?

====================================================
HIGHEST_REVENUE_MONTH
====================================================

Questions asking which month had the highest revenue.

Examples:

Which month had the highest revenue?
What was our best sales month?
Which month performed best?

====================================================
LOWEST_REVENUE_MONTH
====================================================

Questions asking which month had the lowest revenue.

Examples:

Which month had the lowest revenue?
What was our weakest sales month?
Which month performed worst?

====================================================
FORECAST_REVENUE
====================================================

Questions asking for future revenue prediction.

Examples:

What is next month's revenue forecast?
What revenue should we expect?
Predict next month's revenue.
How much revenue are we likely to generate?

====================================================
IMPORTANT
====================================================

Do NOT classify these as analytics:

customers
customer rankings
products
product rankings
regions
geographical areas
locations
orders
customer revenue
product revenue
regional revenue

Those belong to SQL.

Return ONLY the operation name.

Question:
{question}
"""

        valid_operations = {
            "AVERAGE_ORDER_VALUE",
            "STANDARD_DEVIATION",
            "HIGHEST_REVENUE_MONTH",
            "LOWEST_REVENUE_MONTH",
            "FORECAST_REVENUE"
        }

        try:

            response = self.llm.invoke(prompt)

            operation = response.content.strip().upper()

            if operation in valid_operations:
                return operation

        except Exception:
            pass

        return None

    # =====================================================
    # EXECUTION
    # =====================================================

    def run(self, question):

        operation = self.classify_operation(question)

        if operation == "AVERAGE_ORDER_VALUE":

            value = self.analytics.average_order_value()

            return {
                "answer": (
                    f"The average order value is "
                    f"${value:,.2f}."
                )
            }

        if operation == "STANDARD_DEVIATION":

            value = self.analytics.standard_deviation_sales()

            return {
                "answer": (
                    f"The standard deviation of sales amount "
                    f"is ${value:,.2f}."
                )
            }

        if operation == "HIGHEST_REVENUE_MONTH":

            monthly_revenue = (
                self.analytics.monthly_revenue()
            )

            highest_month = monthly_revenue.idxmax()

            highest_revenue = monthly_revenue.max()

            month_name = highest_month.strftime("%B")

            return {
                "answer": (
                    f"{month_name} had the highest revenue "
                    f"with ${highest_revenue:,.2f}."
                )
            }

        if operation == "LOWEST_REVENUE_MONTH":

            monthly_revenue = (
                self.analytics.monthly_revenue()
            )

            lowest_month = monthly_revenue.idxmin()

            lowest_revenue = monthly_revenue.min()

            month_name = lowest_month.strftime("%B")

            return {
                "answer": (
                    f"{month_name} had the lowest revenue "
                    f"with ${lowest_revenue:,.2f}."
                )
            }

        if operation == "FORECAST_REVENUE":

            forecast = (
                self.forecaster.forecast_next_month()
            )

            return {
                "answer": (
                    f"The forecast for next month's revenue "
                    f"is ${forecast:,.2f}."
                )
            }

        return {
            "answer": (
                "I could not determine the requested "
                "analytics."
            )
        }