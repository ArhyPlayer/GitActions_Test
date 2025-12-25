from fastapi import FastAPI, HTTPException
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional

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

@app.get("/time/convert")
async def convert_time(utc_time: str, timezone: str):
    """
    Convert UTC time to specified timezone

    Parameters:
    - utc_time: UTC time in ISO format (e.g., "2024-12-25T15:00:00")
    - timezone: Target timezone (e.g., "Europe/Moscow", "America/New_York")
    """
    try:
        # Parse UTC time
        utc_datetime = datetime.fromisoformat(utc_time.replace('Z', '+00:00'))

        # Ensure it's UTC
        if utc_datetime.tzinfo is None:
            utc_datetime = utc_datetime.replace(tzinfo=ZoneInfo("UTC"))
        elif utc_datetime.tzinfo != ZoneInfo("UTC"):
            # Convert to UTC if it's in different timezone
            utc_datetime = utc_datetime.astimezone(ZoneInfo("UTC"))

        # Convert to target timezone
        target_tz = ZoneInfo(timezone)
        converted_time = utc_datetime.astimezone(target_tz)

        return {
            "utc_time": utc_datetime.isoformat(),
            "target_timezone": timezone,
            "converted_time": converted_time.isoformat(),
            "converted_time_readable": converted_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "utc_offset": converted_time.strftime("%z"),
            "timezone_name": converted_time.strftime("%Z")
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error converting time: {str(e)}. Make sure utc_time is in ISO format and timezone is valid."
        )


