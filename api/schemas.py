import datetime

from pydantic import BaseModel, computed_field, field_serializer
from typing import List, Optional, Literal

from constants import MealMoment, WeekStatus
from utils import is_current, get_current_week_number


class MealDish(BaseModel):
    name: str
    from_restaurant: bool
    is_vegetarian: bool
    is_long_to_prepare: bool


class SeasonDish(BaseModel):
    name: str


class Season(BaseModel):
    name: str
    icon: str
    dishes: List[SeasonDish]


class Dish(BaseModel):
    name: str
    from_restaurant: bool
    is_vegetarian: bool
    is_long_to_prepare: bool
    seasons: List[SeasonDish]


class CreateDish(BaseModel):
    name: str
    from_restaurant: Optional[bool] = None
    vegetarian: Optional[bool] = None
    is_long_to_prepare: Optional[bool] = None
    seasons: List[int]

    class Config:
        from_attributes = True


class Meal(BaseModel):
    type: MealMoment
    dish: MealDish

    @field_serializer("type")
    def serialize_type(self, meal_type: MealMoment, _info):
        return MealMoment(meal_type).name


class Day(BaseModel):
    number: int
    name: str
    date: datetime.datetime
    meals: List[Meal]

    @field_serializer("date")
    def serialize_date(self, date: datetime.datetime, _info):
        return date.strftime("%d/%m")

    @computed_field
    @property
    def is_today(self) -> bool:
        return self.date.date() == datetime.datetime.today().date()


class Week(BaseModel):
    year: int
    number: int
    days: List[Day]
    status: WeekStatus

    @computed_field
    @property
    def is_current(self) -> bool:
        return is_current(self.number)

    @computed_field
    @property
    def is_finished(self) -> bool:
        return (
            self.number < get_current_week_number()
            and self.year <= datetime.date.today().year
        )

    @field_serializer("status")
    def serialize_status(self, status: WeekStatus, _info):
        return WeekStatus(status).name


class WeekAction(BaseModel):
    action: Literal["save", "edit"]
