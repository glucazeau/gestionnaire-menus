import datetime
import enum

from typing import List
from sqlalchemy import String, Enum, Integer, Date, Table, ForeignKey, Column, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session


from database import Base


seasons_dishes = Table(
    "seasons_dishes",
    Base.metadata,
    Column("season_id", ForeignKey("seasons.id")),
    Column("dish_id", ForeignKey("dishes.id")),
)


class Season(Base):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(10))
    icon: Mapped[str] = mapped_column(String(10))
    dishes: Mapped[List["Dish"]] = relationship(
        init=False,
        back_populates="seasons",
        secondary="seasons_dishes",
        order_by="asc(Dish.name)",
    )

    def __repr__(self):
        return f"Season(name={self.name})"


class MealMoment(enum.Enum):
    Matin = 0
    Soir = 1


class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    type = mapped_column(Enum(MealMoment))


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    seasons: Mapped[List[Season]] = relationship(
        back_populates="dishes", secondary="seasons_dishes"
    )
    from_restaurant: Mapped[bool] = Column(Boolean, unique=False, default=False)
    is_vegetarian: Mapped[bool] = Column(Boolean, default=False)

    def __repr__(self):
        return f"Dish(name={self.name})"


class Day(Base):
    __tablename__ = "days"

    number: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(8))
    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    meals: Mapped[List["Meal"]] = relationship()
    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"))
    week_id: Mapped[int] = mapped_column(ForeignKey("weeks.id"))


class WeekStatus(enum.Enum):
    DRAFT = 0
    SAVED = 1


class Week(Base):
    __tablename__ = "weeks"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[int] = mapped_column(Integer, primary_key=True)
    days: Mapped[List["Day"]] = relationship()
    status: Mapped[WeekStatus] = mapped_column(
        Enum(WeekStatus), default=WeekStatus.DRAFT
    )
