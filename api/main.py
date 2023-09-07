from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from typing import List

import dish
import season

from database import SessionLocal, engine


dish.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/dish/", response_model=dish.DishEntity)
def create_dish(new_dish: dish.DishModel, db: Session = Depends(get_db)):
    return dish.create_dish(db=db, dish=new_dish)


@app.get("/dishes", response_model=List[dish.DishModel])
async def get_dishes(db: Session = Depends(get_db)):
    return dish.list_dishes(db)


@app.get("/seasons")
async def seasons():
    return season.list_seasons()
