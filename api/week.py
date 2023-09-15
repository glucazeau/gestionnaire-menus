import datetime

from loguru import logger
from sqlalchemy import and_
from sqlalchemy.orm import Session

from models import Week, Day, Meal, MealMoment, WeekStatus


def get_current_week_number():
    now = datetime.datetime.now()
    return datetime.date(now.year, now.month, now.day).isocalendar()[1]


def is_current(number):
    return number == get_current_week_number()


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


def get_week(db: Session, year, week_number) -> Week:
    logger.info(f"Retrieving week {week_number}/{year}")
    week = (
        db.query(Week)
        .filter(and_(Week.year == year, Week.number == week_number))
        .first()
    )
    if week is None:
        logger.info(f"Initializing week {week_number}/{year}")
        week = Week(year=year, number=week_number, days=[], status=WeekStatus.DRAFT)

        db.add(week)
        db.commit()
        db.refresh(week)
        # get list of days from week number
        days = get_days(year, week_number)
        for day_number, day_name, date in days:
            logger.info(f"Creating day {day_number} - {day_name} - {date}")
            day = Day(
                number=day_number,
                name=day_name,
                date=date,
                meals=[],
                week=week,
            )
            db.add(day)
            db.commit()
            db.refresh(day)

            meals = []
            if day.number in [3, 6, 7]:
                db.add(Meal(type=MealMoment.Midi, day=day))
            db.add(Meal(type=MealMoment.Soir, day=day))

        db.commit()
        db.refresh(week)
    return week


def list_weeks(db: Session):
    return db.query(Week).all()
