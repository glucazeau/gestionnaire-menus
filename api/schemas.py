import datetime

from pydantic import BaseModel, computed_field
from typing import List, Optional

from week import is_current


class Day(BaseModel):
    number: int
    name: str
    date: datetime.datetime


class Week(BaseModel):
    year: int
    number: int
    days: List[Day]

    @computed_field
    @property
    def is_current(self) -> bool:
        return is_current(self.number)


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
    seasons: List[Season]


class CreateDish(BaseModel):
    name: str
    from_restaurant: Optional[bool] = None
    vegetarian: Optional[bool] = None
    seasons: List[int]

    class Config:
        from_attributes = True
