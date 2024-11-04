from datetime import date, timedelta, datetime

def next_weekday(given_date, weekday):
    # day of the week for the given_date, where Mon is 0 and Sun is 6
    current_weekday = given_date.weekday()
    
    # calculate how many days to add to get next weekday
    # if desired weekday is not after current weekday, move to next week
    days_until_next_weekday = (weekday - current_weekday + 7) % 7
    if days_until_next_weekday == 0:
        days_until_next_weekday = 7  # ensure it returns next occurrence, not the current day

    # calculate new date
    next_weekday_date = given_date + timedelta(days=days_until_next_weekday)
    return next_weekday_date

def days_between(date1, date2):
    return abs((date2 - date1).days)

def add_days(date, days):
     return date + timedelta(days=days)
     
def is_weekend(date: datetime) -> bool:
    return date.weekday() >= 5

