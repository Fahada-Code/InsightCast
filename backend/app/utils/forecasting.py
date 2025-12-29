import pandas as pd
from prophet import Prophet
import os

def generate_forecast(file_path: str, days: int = 30) -> pd.DataFrame:
    """
    Loads time-series data from a CSV file, trains a Prophet model,
    and forecasts the next N days.

    Args:
        file_path (str): Path to the CSV file (must have 'ds' and 'y' columns).
        days (int): Number of days to forecast into the future.

    Returns:
        pd.DataFrame: DataFrame containing 'ds', 'yhat', 'yhat_lower', 'yhat_upper'.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at {file_path}")

    # Load data
    df = pd.read_csv(file_path)
    
    # Ensure required columns exist
    if 'ds' not in df.columns or 'y' not in df.columns:
        raise ValueError("CSV must contain 'ds' (date) and 'y' (value) columns.")

    # Convert ds to datetime just in case
    df['ds'] = pd.to_datetime(df['ds'])

    # Initialize and train Prophet model
    m = Prophet()
    m.fit(df)

    # Create future dataframe
    future = m.make_future_dataframe(periods=days)

    # Forecast
    forecast = m.predict(future)

    # Return relevant columns
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
