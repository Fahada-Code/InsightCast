from fastapi import FastAPI
from app.routes import forecast

app = FastAPI(title="Predictive Business Insights Platform")

# Register Routers
app.include_router(forecast.router)

@app.get("/")
def root():
    return {"status": "Backend is running"}
