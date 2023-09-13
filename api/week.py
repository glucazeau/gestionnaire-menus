import datetime


def get_current_week_number():
    now = datetime.datetime.now()
    return datetime.date(now.year, now.month, now.day).isocalendar()[1]


def get_next_week_number():
    pass


def init_week():
    pass
