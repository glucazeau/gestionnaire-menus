import datetime

from typing import List
from sqlalchemy import (
    String,
    Enum,
    Integer,
    Date,
    Table,
    ForeignKey,
    Column,
    Boolean,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from constants import MealMoment, WeekStatus
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


class Meal(Base):
    __tablename__ = "meals"
    __table_args__ = (
        ForeignKeyConstraint(
            ["year", "week_number", "day_number"],
            ["day.year", "day.week_number", "day.number"],
        ),
        ForeignKeyConstraint(
            ["dish_id"],
            ["dishes.id"],
        ),
    )
    type: Mapped[MealMoment] = mapped_column(Enum(MealMoment), primary_key=True)
    year = Column(Integer, nullable=False, primary_key=True)
    week_number = Column(Integer, nullable=False, primary_key=True)
    day_number = Column(Integer, nullable=False, primary_key=True)
    day: Mapped["Day"] = relationship(
        foreign_keys=[year, week_number, day_number], back_populates="meals"
    )
    dish_id = Column(Integer, nullable=True)
    dish: Mapped["Dish"] = relationship(foreign_keys=[dish_id])


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    seasons: Mapped[List[Season]] = relationship(
        back_populates="dishes", secondary="seasons_dishes"
    )
    from_restaurant: Mapped[bool] = Column(Boolean, default=False)
    is_vegetarian: Mapped[bool] = Column(Boolean, default=False)
    is_long_to_prepare: Mapped[bool] = Column(Boolean, default=False)

    def __repr__(self):
        return f"Dish(name={self.name})"


class Week(Base):
    __tablename__ = "week"

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[int] = mapped_column(Integer, primary_key=True)
    days: Mapped[List["Day"]] = relationship()
    status: Mapped[WeekStatus] = mapped_column(
        Enum(WeekStatus), default=WeekStatus.DRAFT
    )


class Day(Base):
    __tablename__ = "day"
    __table_args__ = (
        ForeignKeyConstraint(["week_number", "year"], ["week.number", "week.year"]),
    )
    number: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(8))
    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)

    week_number = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    week: Mapped["Week"] = relationship(
        foreign_keys=[week_number, year], back_populates="days"
    )

    meals: Mapped[List["Meal"]] = relationship()

    def is_weekend(self):
        return self.number in (6, 7)
