import pandas as pd
from prophet import Prophet
import os
from typing import Optional

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names to 'ds' and 'y' using smart detection.
    """
    # 1. Detect Date Column
    date_col = None
    if 'ds' in df.columns:
        date_col = 'ds'
    else:
        # Case-insensitive search for 'date' or 'ds' or 'timestamp'
        for col in df.columns:
            if col.lower() in ['date', 'ds', 'timestamp', 'time']:
                date_col = col
                break
    
    if not date_col:
        raise ValueError("Could not detect a date column (looking for 'ds', 'date', 'timestamp').")

    # 2. Detect Target Column
    target_col = None
    if 'y' in df.columns:
        target_col = 'y'
    else:
        # Potential targets (excluding date column)
        potential_targets = [c for c in df.columns if c != date_col]
        
        # Check for explicit 'y' match first
        for col in potential_targets:
            if col.lower() == 'y':
                target_col = col
                break
        
        if not target_col:
            # Check for generic value names
            common_names = ['value', 'sales', 'revenue', 'quantity', 'amount', 'close', 'price']
            for col in potential_targets:
                if col.lower() in common_names:
                    target_col = col
                    break
            
            # If still not found, pick the first numeric column
            if not target_col:
                numeric_cols = df[potential_targets].select_dtypes(include=['number', 'float', 'int']).columns
                if len(numeric_cols) > 0:
                    target_col = numeric_cols[0]

    if not target_col:
        raise ValueError("Could not detect a numeric target column. Please ensure one exists.")

    # 3. Rename and Filter
    df = df.rename(columns={date_col: 'ds', target_col: 'y'})
    
    # Ensure y is numeric
    df['y'] = pd.to_numeric(df['y'], errors='coerce')
    df = df.dropna(subset=['y'])
    
    return df[['ds', 'y']]

def generate_forecast(
    file_path: str | pd.DataFrame,
    days: int = 30,
    seasonality_mode: str = 'additive',
    growth: str = 'linear',
    daily_seasonality: bool = False,
    weekly_seasonality: bool = False,
    yearly_seasonality: bool = False,
    holidays: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Loads time-series data from a CSV file or DataFrame, trains a Prophet model with custom settings,
    and forecasts the next N days.
    """
    # Load data
    if isinstance(file_path, str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found at {file_path}")
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Failed to read CSV: {str(e)}")
    elif isinstance(file_path, pd.DataFrame):
        df = file_path
    else:
        raise ValueError("file_path must be a string path or pandas DataFrame")
    
    # Ensure required columns exist (if not already preprocessed, though we expect it to be)
    if 'ds' not in df.columns or 'y' not in df.columns:
         # Try simplifying, but ideally it should have been done
        pass
        # raise ValueError("CSV must contain 'ds' (date) and 'y' (value) columns.")

    # Convert ds to datetime
    try:
        df['ds'] = pd.to_datetime(df['ds'])
    except Exception:
        raise ValueError("Could not parse 'ds' column as dates.")
        
    if df['ds'].dt.tz is not None:
        df['ds'] = df['ds'].dt.tz_localize(None)

    # Initialize Prophet model with custom parameters
    m = Prophet(
        seasonality_mode=seasonality_mode,
        growth=growth,
        daily_seasonality=daily_seasonality,
        weekly_seasonality=weekly_seasonality,
        yearly_seasonality=yearly_seasonality,
        holidays=holidays
    )
    
    m.fit(df)

    # Create future dataframe
    future = m.make_future_dataframe(periods=days)

    # Forecast
    forecast = m.predict(future)

    # Return relevant columns
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
