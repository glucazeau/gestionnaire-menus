from abc import ABC, abstractmethod
from models import Day, Week, Dish
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
        day: Day,
        week: Week,
    ):
        pass


class NoLongDishOnWeekDay(Rule):
    name = "No long dish on week day"

    def valid(self, dish: Dish, day: Day, week: Week) -> bool:
        return not dish.is_long_to_prepare or day.is_weekend()


rules = [NoLongDishOnWeekDay()]


def validate_dish(dish: Dish, day: Day, week: Week) -> (bool, str):
    for rule in rules:
        result = rule.valid(dish, day, week)
        if not result:
            return False, rule.name
    return True, "OK"
