from sqlalchemy.orm import Session
from loguru import logger

import models
import schemas


def list_dishes(db: Session):
    return db.query(models.Dish)


def create_dish(db: Session, dish: schemas.CreateDish):
    logger.info(f"Creating dish from body {dish}")
    logger.debug(f"Retrieving season objects from ids {dish.seasons}")
    get_seasons = (
        db.query(models.Season).filter(models.Season.id.in_(dish.seasons)).all()
    )
    logger.debug(f"Found seasons: {get_seasons}")
    new_dish = models.Dish(
        name=dish.name,
        from_restaurant=dish.from_restaurant,
        seasons=get_seasons,
        is_vegetarian=dish.vegetarian,
    )
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish
