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

@app.get("/date")
async def get_server_date():
    """Return current server date in various formats"""
    current_date = datetime.now().date()
    return {
        "date": current_date.isoformat(),
        "formatted": current_date.strftime("%Y-%m-%d"),
        "readable": current_date.strftime("%B %d, %Y"),
        "day": current_date.day,
        "month": current_date.month,
        "year": current_date.year,
        "weekday": current_date.strftime("%A")
    }

@app.get("/date/iso")
async def get_date_iso():
    """Return current date in ISO format"""
    return {"date": datetime.now().date().isoformat()}

@app.get("/date/formatted")
async def get_date_formatted():
    """Return current date in readable format"""
    current_date = datetime.now().date()
    return {"date": current_date.strftime("%B %d, %Y")}

@app.get("/date/today")
async def get_today():
    """Return today's date information"""
    today = datetime.now().date()
    return {
        "today": today.isoformat(),
        "is_weekend": today.weekday() >= 5,  # 5 = Saturday, 6 = Sunday
        "day_of_week": today.strftime("%A"),
        "day_of_year": today.timetuple().tm_yday
    }


