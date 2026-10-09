import pandas as pd


class RevenueForecaster:

    def __init__(self):

        self.sales = pd.read_csv(
            "data/sales.csv"
        )

        self.sales["order_date"] = pd.to_datetime(
            self.sales["order_date"]
        )

    def forecast_next_month(self):

        monthly_revenue = (
            self.sales
            .set_index("order_date")
            .resample("ME")["sales_amount"]
            .sum()
        )

        if monthly_revenue.empty:
            raise ValueError(
                "No sales data is available for forecasting."
            )

        # Simple baseline forecast:
        # average of historical monthly revenue.
        forecast = monthly_revenue.mean()

        return float(forecast)