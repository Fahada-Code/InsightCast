import pandas as pd
from prophet import Prophet

def run_forecast(csv_path: str, periods: int = 30):
    # Load data
    df = pd.read_csv(csv_path)

    # Prophet requires columns: ds (date), y (value)
    df["ds"] = pd.to_datetime(df["ds"])

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
