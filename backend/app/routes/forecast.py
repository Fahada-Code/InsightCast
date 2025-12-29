from fastapi import APIRouter, HTTPException, Query
from app.utils.forecasting import generate_forecast
import os
import pandas as pd

router = APIRouter()

# Path to the sample data - assuming relative path from where main.py runs
# Adjust this path based on where you run uvicorn from. 
# If running from 'backend', it is 'data/sample_data.csv'
DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "sample_data.txt")

@router.get("/forecast", tags=["Forecasting"])
async def get_forecast(days: int = Query(30, description="Number of days to forecast")):
    """
    Generate a forecast using the Prophet model based on local CSV data.
    """
    if not os.path.exists(DATA_FILE_PATH):
        raise HTTPException(status_code=404, detail="Data file not found. Please ensure 'data/sample_data.csv' exists.")

    try:
        # Generate forecast
        forecast_df = generate_forecast(DATA_FILE_PATH, days=days)
        
        # Convert to dict for JSON response (oriented records usually easiest for frontend)
        # However, for pure timeseries, list of dicts is standard
        result = forecast_df.tail(days).to_dict(orient="records")
        
        return {
            "messsage": f"Forecast generated for next {days} days",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
