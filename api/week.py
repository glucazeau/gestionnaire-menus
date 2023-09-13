import datetime


def get_current_week_number():
    now = datetime.datetime.now()
    return datetime.date(now.year, now.month, now.day).isocalendar()[1]


def get_next_week_number():
    pass


def get_days(week, year):
    d = f"{year}-W{week}"
    monday = datetime.datetime.strptime(d + "-1", "%Y-W%W-%w")
    days = [monday]
    for i in range(1, 7):
        days.append(monday + datetime.timedelta(days=i))
    return days


def init_week():
    pass
