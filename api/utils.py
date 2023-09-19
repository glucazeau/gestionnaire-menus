import datetime

from typing import Tuple


def get_current_week_number():
    now = datetime.datetime.now()
    return datetime.date(now.year, now.month, now.day).isocalendar()[1]


def is_current(number):
    return number == get_current_week_number()


def get_previous_week_number(year, week_number) -> Tuple[int, int]:
    previous_week_year = year
    previous_week_number = week_number - 1
    if previous_week_number < 1:
        previous_week_number = 52
        previous_week_year = year - 1
    return previous_week_year, previous_week_number


def get_next_week_number():
    pass


def get_days(year, week):
    d = f"{year}-W{week}"
    monday = datetime.datetime.strptime(d + "-1", "%Y-W%W-%w")
    days = [(1, "lundi", monday)]
    for name, number in {
        "mardi": 2,
        "mercredi": 3,
        "jeudi": 4,
        "vendredi": 5,
        "samedi": 6,
        "dimanche": 7,
    }.items():
        days.append((number, name, monday + datetime.timedelta(days=number - 1)))
    return days
