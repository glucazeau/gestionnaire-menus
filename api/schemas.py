import datetime

from pydantic import BaseModel
from typing import List, Optional


class Day(BaseModel):
    number: int
    name: str
    date: datetime.datetime


class Week(BaseModel):
    year: int
    number: int
    is_current: bool = False
    days: List[Day]


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
