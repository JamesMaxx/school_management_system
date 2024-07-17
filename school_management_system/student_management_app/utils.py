# utils.py students_attendance_calendar
from datetime import date, timedelta

def generate_weekday_dates(start_date, end_date):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday to Friday
            dates.append(current_date)
        current_date += timedelta(days=1)
    return dates
