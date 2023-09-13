from pydantic import BaseModel
from typing import List, Optional


class SeasonDish(BaseModel):
    name: str


class Season(BaseModel):
    name: str
    icon: str
    dishes: List[SeasonDish]


class Dish(BaseModel):
    name: str
    from_restaurant: bool
    seasons: List[Season]


class CreateDish(BaseModel):
    name: str
    from_restaurant: Optional[bool] = None
    seasons: List[int]

    class Config:
        from_attributes = True
