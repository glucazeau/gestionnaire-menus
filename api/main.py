import datetime

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqlalchemy.orm import Session
from typing import List

import schemas
import dish
import season
import week
import data

from utils import get_current_week_number

from database import SessionLocal, engine, Base

logger.info("Creating tables")
Base.metadata.create_all(bind=engine)

logger.info(f"Created tables : {Base.metadata.tables.keys()}")


app = FastAPI()

origins = [
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/init", status_code=201)
async def init(db: Session = Depends(get_db)):
    data.init_seasons(db)
    data.init_dishes(db)
    return "Initial data inserted"


@app.post("/dish/", response_model=schemas.Dish)
def create_dish(new_dish: schemas.CreateDish, db: Session = Depends(get_db)):
    return dish.create_dish(db=db, dish=new_dish)


@app.get("/dishes", response_model=List[schemas.Dish])
async def get_dishes(db: Session = Depends(get_db)):
    return dish.list_dishes(db)


@app.get("/seasons", response_model=List[schemas.Season])
async def get_seasons(db: Session = Depends(get_db)):
    return season.list_seasons(db)


@app.get("/week", response_model=List[schemas.Week])
async def get_weeks(db: Session = Depends(get_db)):
    return week.list_weeks(db)


@app.get("/week/{year}/{number}", response_model=schemas.Week)
async def get_week(year, number, db: Session = Depends(get_db), generate: bool = False):
    return week.get_week_menus(db, year, number, generate)


@app.get("/week/current", response_model=schemas.Week)
async def get_current_week(db: Session = Depends(get_db), generate: bool = False):
    now = datetime.datetime.now()
    return week.get_week_menus(db, now.year, get_current_week_number(), generate)


@app.post("/week/{year}/{number}", response_model=schemas.Week)
async def change_week_status(
    year, number, action: schemas.WeekAction, db: Session = Depends(get_db)
):
    status = week.WeekStatus.SAVED if action.action == "save" else week.WeekStatus.DRAFT
    week.set_week_status(db, year, number, status)
    return week.get_week_menus(db, year, number)
