from pydantic import BaseModel
from typing import List

from models import Season


class SeasonDish(BaseModel):
    name: str


class Dish(BaseModel):
    name: str
    seasons: List[Season]


class CreateDish(BaseModel):
    name: str
    seasons: List[int]

    class Config:
        from_attributes = True


class Season(BaseModel):
    name: str
    icon: str
    dishes: List[SeasonDish]
