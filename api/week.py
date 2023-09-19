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
                db.add(Meal(type=MealMoment.Midi, day=day, dish=None))
            db.add(Meal(type=MealMoment.Soir, day=day, dish=None))

        db.commit()
        db.refresh(week)
    return week


def list_weeks(db: Session):
    return db.query(Week).order_by(Week.year.asc(), Week.number.asc()).all()


def get_week_menus(db: Session, year, week_number, generate):
    logger.info(f"Generating menu for week {week_number}/{year}")
    week = get_week(db, year, week_number)

    logger.debug("Listing available meals")
    dishes = list_dishes(db)
    logger.debug(f"{len(dishes)} meals found")

    for day in week.days:
        for meal in day.meals:
            if can_generate(week.status, meal, generate):
                logger.debug(f"Choosing dish for {day.name} ({meal.type})")
                random_dish = random.choice(dishes)
                logger.debug(f"Chosen dish is {random_dish.name}")
                meal.dish = random_dish
                db.add(meal)
                dishes.remove(random_dish)
            else:
                logger.warning("Cannot generate menus")

    db.commit()
    db.refresh(week)
    logger.debug(f"Menu for week {week_number}/{year} completed")
    return week


def can_generate(week_status, meal, generate):
    return week_status == WeekStatus.DRAFT and (meal.dish is None or generate)
