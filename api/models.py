import datetime
import enum

from typing import List
from sqlalchemy import (
    create_engine,
    String,
    Enum,
    Integer,
    Date,
    Table,
    ForeignKey,
    Column,
)
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from database import Base


association_table = Table(
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


@listens_for(Season.__table__, "after_create")
def insert_initial_values(target, connection, **kwargs):
    session = Session(bind=connection)
    session.add(Season("Printemps", "🌱"))
    session.add(Season("Été", "☀"))
    session.add(Season("Automne", "🍂"))
    session.add(Season("Hiver", "🌨️"))
    session.commit()


class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    seasons: Mapped[List[Season]] = relationship(
        back_populates="dishes", secondary="seasons_dishes"
    )

    def __repr__(self):
        return f"Dish(name={self.name})"


class Day:
    __tablename__ = "days"

    number: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(8))
    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    meals: Mapped[List["Meal"]] = relationship()


class WeekStatus(enum.Enum):
    DRAFT = 0
    SAVED = 1


class Week:
    __tablename__ = "weeks"

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[int] = mapped_column(Integer, primary_key=True)
    days: Mapped[List["Day"]] = relationship()
    status: Mapped[WeekStatus] = mapped_column(
        Enum(WeekStatus), default=WeekStatus.DRAFT
    )
