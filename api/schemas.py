import datetime

from pydantic import BaseModel, computed_field, field_serializer, FieldSerializationInfo
from typing import List, Optional, Any

from week import is_current


class Day(BaseModel):
    number: int
    name: str
    date: datetime.datetime

    @field_serializer("date")
    def serialize_date(self, date: datetime.datetime, _info):
        return date.strftime("%d/%m")


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
