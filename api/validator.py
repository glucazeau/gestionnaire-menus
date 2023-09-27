from abc import ABC, abstractmethod
from models import Day, Week, Dish, Meal, MealMoment
from dataclasses import dataclass


@dataclass
class Rule(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def valid(
        self,
        dish: Dish,
        meal: Meal,
        day: Day,
        week: Week,
    ):
        pass


class NoLongDishOnWeekDay(Rule):
    name = "No long dish on week day"

    def valid(self, dish: Dish, meal: Meal, day: Day, week: Week) -> bool:
        return not dish.is_long_to_prepare or day.is_weekend()


class PaidDishOnlyOnWeekendNights(Rule):
    name = "Paid dishes are for Friday or weekend nights"

    def valid(self, dish: Dish, meal: Meal, day: Day, week: Week) -> bool:
        return not dish.from_restaurant or (
            (day.number == 5 or day.is_weekend()) and meal.type is MealMoment.Soir
        )


rules = [NoLongDishOnWeekDay(), PaidDishOnlyOnWeekendNights()]


def validate_dish(dish: Dish, meal: Meal, day: Day, week: Week) -> (bool, str):
    logger.debug(f"Validating {dish}")
    for rule in rules:
        result = rule.valid(dish, meal, day, week)
        logger.debug(f"  with rule {rule.name}: {result}")
        if not result:
            return False, rule.name
    logger.debug("Dish is valid")
    return True, "OK"
