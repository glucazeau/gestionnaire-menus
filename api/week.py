import datetime
import random

from loguru import logger
from sqlalchemy import and_
from sqlalchemy.orm import Session

from constants import MealMoment, WeekStatus
from utils import get_days
from models import Week, Day, Meal
from dish import list_dishes


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

            if day.number in [3, 6, 7]:
                db.add(Meal(type=MealMoment.Midi, day=day))
            db.add(Meal(type=MealMoment.Soir, day=day))

        db.commit()
        db.refresh(week)
    return week


def list_weeks(db: Session):
    return db.query(Week).order_by(Week.year.asc(), Week.number.asc()).all()
