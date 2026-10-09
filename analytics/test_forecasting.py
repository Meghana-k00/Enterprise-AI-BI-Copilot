from forecasting import RevenueForecaster


forecaster = RevenueForecaster()

forecast = forecaster.forecast_next_month()

print("\nNext Month Revenue Forecast:")
print(forecast)