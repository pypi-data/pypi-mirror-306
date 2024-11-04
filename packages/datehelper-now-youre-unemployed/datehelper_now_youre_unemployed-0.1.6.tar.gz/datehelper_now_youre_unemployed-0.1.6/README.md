# Python Package Exercise

An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.


# datehelper
![Event Logger Workflow](https://github.com/software-students-fall2024/3-python-package-now-youre-unemployed/actions/workflows/event-logger.yml/badge.svg)

**A Python utility package for date manipulation**

---

## Overview

`datehelper` is a Python package to help with simple date manipulation tasks.  The functions included can help calculate date differences, check for weekends, and help find the date of the next requested weekday.  This package can streamline date-related logic in Python projects.

---

## Features

- **days_between(date1, date2)**: Returns the number of days between two dates.
- **add_days(date, days)**: Returns a new date given a date and a number of days.
- **is_weekend(date)**: Checks if a given date is a weekend (Saturday or Sunday).
- **next_weekday(date, weekday)**: Returns the date of the next given weekday.

---

## Installation

1. `pip`:

```bash

pip install datehelper

```

2. Import the functions into your code:

```bash

from datehelper import days_between, add_days, is_weekend, next_weekday

```
---

## Usage Examples

1. **`next_weekday(given_date: date, weekday: int) -> date`**  
   Returns the next occurrence of a specified weekday from a given date. Weekdays are represented by integers where Monday is 0 and Sunday is 6.
    ```python
   print(next_weekday(date(2024, 11, 4), 3))

2. **`days_between(date1: date, date2: date) -> int`**  
   Calculates the absolute number of days between two dates.
    ```python
   print(days_between(date(2023, 1, 1), date(2023, 1, 10)))


3. **`add_days(start_date: date, days: int) -> date`**  
   Returns a new date that is a specified number of days after the given start date.
    ```python
   print(add_days(date(2023, 1, 1), 10))

4. **`is_weekend(check_date: datetime) -> bool`** 
   Checks if a given date falls on a weekend (Saturday or Sunday).
    ```python
   print(is_weekend(datetime(2024, 11, 3)))


**For a complete example, see [`example_date.py`](./example_date.py).**

---

## Setup

1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone datehelper repository 
```

2. Next cd into where the repository folder is located on your local machine:

```bash
cd local/path/to/datehelper
```

3. Thirdly install pipenv if you have not already using and then activate the virtual environment: 

```bash
pip install pipenv 
pipenv shell
```

4. Install the dependencies 

```bash
pipenv install --dev
```

5. Build the package

```bash
python -m build
```

6. If you have already built the package make sure to clean it: 

```bash
rm -rf dist src/*.egg-info
```

7. To run tests: 

```bash
pipenv run pytest
```
---

## Team Members

- Shray Awasti - [Github Profile](https://github.com/shrayawasti)
- Toshi Troyer - [Github Profile](https://github.com/toshiHTroyer)
- Ethan Cheng - [Github Profile](https://github.com/ethanhcheng)
- Joseph Hwang - [Github Profile](https://github.com/josephnyu)
---
