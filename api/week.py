import datetime
import random

from loguru import logger
from sqlalchemy import and_
from sqlalchemy.orm import Session

from constants import MealMoment, WeekStatus
from utils import get_days, get_previous_week_number
from models import Week, Day, Meal
from dish import list_dishes


def get_week(db: Session, year, week_number) -> Week:
    logger.info(f"Retrieving week {week_number}/{year}")
    return (
        db.query(Week)
        .filter(and_(Week.year == year, Week.number == week_number))
        .first()
    )


def init_week(db: Session, year, week_number) -> Week:
    week = get_week(db, year, week_number)
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


def get_previous_week_dishes(db: Session, week: Week):
    year, number = get_previous_week_number(week.year, week.number)
    previous_week = get_week(db, year, number)

    if previous_week is None:
        return []
    else:
        return [meal.dish for day in previous_week.days for meal in day.meals]


def get_week_menus(db: Session, year, week_number, generate):
    logger.info(f"Generating menu for week {week_number}/{year}")
    week = init_week(db, year, week_number)

    logger.info("Listing previous week dishes")
    previous_week_dishes = get_previous_week_dishes(db, week)

    logger.debug("Listing available dishes")
    dishes = list_dishes(db, previous_week_dishes)
    logger.debug(f"{len(dishes)} meals found")

    for day in week.days:
        for meal in day.meals:
            if can_generate(week.status, meal, generate):
                logger.debug(f"Choosing dish for {day.name} ({meal.type.name})")
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


def can_generate(week_status: WeekStatus, meal: Meal, generate: bool):
    logger.debug(f"{week_status} - {meal.dish} - {generate}")
    return week_status == WeekStatus.DRAFT and (meal.dish is None or generate)
