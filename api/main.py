from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from typing import List

import dish
import schemas
import season

from database import SessionLocal, engine, Base


Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/dish/", response_model=schemas.Dish)
def create_dish(new_dish: schemas.CreateDish, db: Session = Depends(get_db)):
    return dish.create_dish(db=db, dish=new_dish)


@app.get("/dishes", response_model=List[schemas.Dish])
async def get_dishes(db: Session = Depends(get_db)):
    return dish.list_dishes(db)


@app.get("/seasons", response_model=List[schemas.Season])
async def get_seasons(db: Session = Depends(get_db)):
    return season.list_seasons(db)
