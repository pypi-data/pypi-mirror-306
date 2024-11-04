from datehelper import days_between, add_days, is_weekend, next_weekday
import pytest
from datetime import date, datetime
from datehelper.core import next_weekday

# define test cases for next_weekday function
def test_next_weekday_later_same_week():
    # checks to find the next Thursday from a Monday
    assert next_weekday(date(2024, 11, 4), 3) == date(2024, 11, 7), "Should be the next Thursday in the same week"

def test_next_weekday_early_next_week():
    # checks to find the next Monday from a Friday
    assert next_weekday(date(2024, 11, 8), 0) == date(2024, 11, 11), "Should be the next Monday in the following week"

def test_next_weekday_already_that_day():
    # checks to skip to next week if it's already on the given weekday
    assert next_weekday(date(2024, 11, 6), 2) == date(2024, 11, 13), "Should be the next Wednesday in the following week, not the current one"

def test_add_days_basic():
    assert add_days(date(2023, 1, 1), 10) == date(2023, 1, 11)

def test_add_days_end_of_month():
    assert add_days(date(2023, 1, 1), 30) == date(2023, 1, 31)

def test_add_days_leap_year():
    assert add_days(date(2023, 3, 1), 365) == date(2024, 2, 29)

def test_days_between():
    assert days_between(date(2023, 1, 1), date(2023, 1, 10)) == 9

def test_days_between_same_date():
    assert days_between(date(2023, 1, 1), date(2023, 1, 1)) == 0

def test_days_between_reverse_order():
    assert days_between(date(2023, 1, 10), date(2023, 1, 1)) == 9

def test_is_weekend_on_weekday():
    date = datetime(2024, 10, 30)
    assert is_weekend(date) == False
    
def test_is_weekend_on_saturday():
    chosen_date = date(2024, 11, 2)
    assert is_weekend(chosen_date) == True
    
def test_is_weekend_on_sunday():
    chosen_date = date(2024, 11, 3)
    assert is_weekend(chosen_date) == True