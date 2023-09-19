from loguru import logger
from typing import List
from sqlalchemy.orm import Session

import models
import schemas


def list_dishes(db: Session, exclude_dishes: List[models.Dish] = None):
    if exclude_dishes is None:
        exclude_dish_ids = []
    else:
        exclude_dish_ids = [dish.id for dish in exclude_dishes]
        logger.debug(f"Excluding dish IDs {exclude_dish_ids}")

    dishes = db.query(models.Dish).where(models.Dish.id.not_in(exclude_dish_ids)).all()
    return dishes


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
        is_long_to_prepare=dish.is_long_to_prepare,
    )
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish
