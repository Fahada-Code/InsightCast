from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from app.utils.forecasting import generate_forecast, normalize_columns
import os
import io
import pandas as pd

router = APIRouter()

# Data directory path
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

@router.post("/forecast", tags=["Forecasting"])
async def get_forecast(
    file: UploadFile = File(...),
    days: int = Query(30, description="Number of days to forecast"),
    seasonality_mode: str = Query('additive', enum=['additive', 'multiplicative']),
    growth: str = Query('linear', enum=['linear', 'flat']),
    daily_seasonality: bool = False,
    weekly_seasonality: bool = False,
    yearly_seasonality: bool = False
):
    """
    Generate a forecast using the Prophet model based on uploaded CSV data.
    """
    # Read file content
    contents = await file.read()
    
    try:
        # Try reading as CSV
        df = pd.read_csv(io.BytesIO(contents))
    except Exception:
        # Try with different encoding if default fails
        try:
            df = pd.read_csv(io.BytesIO(contents), encoding='latin1')
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid CSV file. Could not parse.")

    # Normalize columns
    try:
        df = normalize_columns(df)
    except ValueError as e:
         raise HTTPException(status_code=400, detail=str(e))

    # Save the standardized file
    file_location = os.path.join(DATA_DIR, f"clean_{file.filename}")
    df.to_csv(file_location, index=False)

    try:
        # Generate analysis (Forecast + Anomalies + Metrics)
        analysis_result = generate_forecast(
            file_path=file_location,
            days=days,
            seasonality_mode=seasonality_mode,
            growth=growth,
            daily_seasonality=daily_seasonality,
            weekly_seasonality=weekly_seasonality,
            yearly_seasonality=yearly_seasonality
        )
        
        forecast_df = analysis_result["forecast"]
        anomalies_df = analysis_result["anomalies"]
        metrics = analysis_result["metrics"]
        insights = analysis_result["insights"]
        
        # Prepare result for JSON response
        # Full forecast series (History + Future)
        forecast_data = forecast_df.to_dict(orient="records")
        
        # Anomalies list
        anomalies_data = anomalies_df.to_dict(orient="records")
        
        return {
            "message": f"Analysis complete. Forecasted {days} days.",
            "row_count": len(df),
            "parameters": {
                "seasonality_mode": seasonality_mode,
                "growth": growth,
            },
            "metrics": metrics,
            "anomalies": anomalies_data,
            "insights": insights,
            "data": forecast_data  # Returning full data now, not just tail
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecasting error: {str(e)}")
