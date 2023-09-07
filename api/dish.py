from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import MappedAsDataclass, Session, DeclarativeBase



class Base(MappedAsDataclass, DeclarativeBase):
    pass

class DishModel(BaseModel):
    name: str


class DishEntity(Base):
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]


#def list_dishes():
    #return [
    #    DishEntity(name="Pâtes carbonara"),
    #    DishEntity(name="Spaghetti bolognaise"),
    #    DishEntity(name="Sushi"),
    #    DishEntity(name="Pizza"),
#]


def list_dishes(db: Session):
    return db.query(DishEntity)


def create_dish(db: Session, dish: DishModel):
    new_dish = DishEntity(name=dish.name)
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish
