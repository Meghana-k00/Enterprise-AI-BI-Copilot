import pandas as pd


class AnalyticsEngine:

    def __init__(self):

        self.sales = pd.read_csv(
            "data/sales.csv"
        )

        self.sales["order_date"] = pd.to_datetime(
            self.sales["order_date"]
        )
    def total_revenue(self):
        return self.sales["sales_amount"].sum()

    def revenue_by_region(self):
        return (
            self.sales
            .groupby("region")["sales_amount"]
            .sum()
        )

    def monthly_revenue(self):

        monthly = (
            self.sales
            .set_index("order_date")
            .resample("ME")["sales_amount"]
            .sum()
        )

        return monthly

    def average_order_value(self):

        return self.sales[
            "sales_amount"
        ].mean()

    def standard_deviation_sales(self):

        return self.sales[
            "sales_amount"
        ].std()