import os
from app.utils.forecasting import generate_forecast
import pytest

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Backend is running"}

def test_forecast_upload_success(client, sample_csv):
    with open(sample_csv, "rb") as f:
        response = client.post(
            "/forecast?days=10",
            files={"file": ("test_sample.csv", f, "text/csv")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 10
    assert "timestamp" not in data["data"][0] # checking structure
    assert "ds" in data["data"][0]

def test_forecast_missing_file(client):
    response = client.post("/forecast?days=10")
    # FastAPI automatically handles missing required fields with 422
    assert response.status_code == 422

def test_forecast_invalid_columns(client, setup_data_dir):
    filename = "data/invalid.csv"
    with open(filename, "w") as f:
        f.write("unknown_col\n100") # Single column, definitely no date
    
    with open(filename, "rb") as f:
        response = client.post(
            "/forecast?days=10",
            files={"file": ("invalid.csv", f, "text/csv")}
        )
    assert response.status_code == 400
    # Our smart detection gives a specific error when date col isn't found
    assert "Could not detect a date column" in response.json()["detail"]

def test_advanced_parameters(client, sample_csv):
    with open(sample_csv, "rb") as f:
        response = client.post(
            "/forecast?days=5&seasonality_mode=multiplicative&growth=linear",
            files={"file": ("test_sample.csv", f, "text/csv")}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["parameters"]["seasonality_mode"] == "multiplicative"
