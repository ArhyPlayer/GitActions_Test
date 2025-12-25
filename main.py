from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Test Backend", description="Simple test backend returning server time")

@app.get("/")
async def root():
    return {"message": "Test backend is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/time")
async def get_server_time():
    """Return current server time"""
    current_time = datetime.now()
    return {
        "server_time": current_time.isoformat(),
        "timestamp": int(current_time.timestamp()),
        "timezone": str(current_time.tzinfo) if current_time.tzinfo else "UTC"
    }


