# test_pipeline.py
from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt
import os

# Updated imports to match actual codebase
from app.utils.forecasting import normalize_columns as preprocess_csv
from app.utils.forecasting import generate_forecast

def plot_actual_fit_forecast(
    df_clean: pd.DataFrame,
    forecast: pd.DataFrame,
    last_n_points: int | None = 300,
) -> None:
    """
    Plot:
      - Actual (ds, y)
      - In-sample fitted yhat over historical ds
      - Future forecast yhat (after last actual date)
      - Uncertainty intervals for future
    """

    # Ensure datetime & sorting
    df_clean = df_clean.copy()
    df_clean["ds"] = pd.to_datetime(df_clean["ds"], errors="coerce")
    df_clean = df_clean.dropna(subset=["ds", "y"]).sort_values("ds").reset_index(drop=True)

    forecast = forecast.copy()
    forecast["ds"] = pd.to_datetime(forecast["ds"], errors="coerce")
    forecast = forecast.dropna(subset=["ds"]).sort_values("ds").reset_index(drop=True)

    if df_clean.empty:
        raise ValueError("df_clean is empty after cleaning. Check preprocess_csv output.")
    if forecast.empty:
        raise ValueError("forecast is empty. Check generate_forecast output.")

    last_actual_date = df_clean["ds"].max()

    # Optional zoom window based on last_n_points of ACTUAL data
    if last_n_points is not None and len(df_clean) > last_n_points:
        start_date = df_clean.iloc[-last_n_points]["ds"]
        df_plot = df_clean[df_clean["ds"] >= start_date].copy()
    else:
        df_plot = df_clean

    # Keep only forecast rows that cover the plot window (and a bit beyond)
    forecast_plot = forecast[forecast["ds"] >= df_plot["ds"].min()].copy()

    # Split forecast into in-sample (<= last actual) and future (> last actual)
    fcst_in_sample = forecast_plot[forecast_plot["ds"] <= last_actual_date].copy()
    fcst_future = forecast_plot[forecast_plot["ds"] > last_actual_date].copy()

    plt.figure(figsize=(12, 6))

    # Actual
    plt.plot(df_plot["ds"], df_plot["y"], label="Actual", linewidth=2)

    # In-sample fitted values (model fit over history)
    if not fcst_in_sample.empty and "yhat" in fcst_in_sample.columns:
        plt.plot(fcst_in_sample["ds"], fcst_in_sample["yhat"], label="Fitted (in-sample)", linewidth=2)

    # Future forecast
    if not fcst_future.empty and "yhat" in fcst_future.columns:
        plt.plot(fcst_future["ds"], fcst_future["yhat"], label="Forecast (future)", linewidth=2)

        # Uncertainty band (future)
        if {"yhat_lower", "yhat_upper"}.issubset(fcst_future.columns):
            plt.fill_between(
                fcst_future["ds"],
                fcst_future["yhat_lower"],
                fcst_future["yhat_upper"],
                alpha=0.2,
                label="Uncertainty (future)",
            )

    plt.axvline(last_actual_date, linestyle="--", linewidth=1)
    plt.title("Actual vs Fitted vs Future Forecast")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.tight_layout()
    # plt.show() # Commented out show for CI/Test environment, logic is what matters

def main() -> None:
    # Use existing sample data path relative to backend root
    sample_file = "data/sample_data.txt" 
    # Or create dummy if not exists
    if not os.path.exists(sample_file):
        print(f"Sample file {sample_file} not found, creating dummy...")
        os.makedirs("data", exist_ok=True)
        with open(sample_file, "w") as f:
            f.write("ds,y\n2023-01-01,100\n2023-01-02,110\n2023-01-03,105")

    try:
        df_raw = pd.read_csv(sample_file)
        df_clean = preprocess_csv(df_raw)
        
        required_cols = {"ds", "y"}
        missing = required_cols - set(df_clean.columns)
        if missing:
            raise ValueError(f"preprocess_csv must return columns {required_cols}. Missing: {missing}")
        
        df_clean = df_clean.copy()
        df_clean["ds"] = pd.to_datetime(df_clean["ds"], errors="coerce")
        df_clean["y"] = pd.to_numeric(df_clean["y"], errors="coerce")
        
        before = len(df_clean)
        df_clean = df_clean.dropna(subset=["ds", "y"]).sort_values("ds").reset_index(drop=True)
        after = len(df_clean)
        
        print("Preprocessed Data (head):")
        print(df_clean.head())
        print(f"Rows before dropna: {before}, after: {after}")
        
        if df_clean.isnull().values.any():
            print("Warning: There are still missing values after cleaning.")
            
        periods = 30
        forecast = generate_forecast(df_clean, days=periods)
        
        print("Forecast (head):")
        print(forecast.head())
        
        # Validating output columns
        assert "yhat" in forecast.columns
        assert "ds" in forecast.columns
        print("Test passed successfully!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        # Re-raise to fail pytest
        raise e

# Pytest entry point
def test_pipeline():
    main()

if __name__ == "__main__":
    main()
