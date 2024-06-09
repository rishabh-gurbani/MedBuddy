from datetime import datetime, timedelta
from pytz import timezone

def roundtime():
    ist_timezone = timezone('Asia/Kolkata')
    current_time = datetime.now(ist_timezone)
    current_hour = current_time.hour
    current_minute = current_time.minute

    # Round the time to the nearest half hour
    if current_minute < 15:
        rounded_minute = 0
    elif current_minute < 45:
        rounded_minute = 30
    else:
        rounded_minute = 0
        current_hour += 1

    # Format the rounded time as a string in the desired format
    rounded_time = f"{current_hour:02d}{rounded_minute:02d}"

    # Check if the rounded time is before 1000 hours
    if current_hour < 10:
        rounded_time = "1000"

    # Get the day name
    day_name = current_time.strftime("%A")

    return rounded_time, day_name

