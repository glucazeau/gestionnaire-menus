from loguru import logger
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Session

from database import Base
from models import Season, Dish, seasons_dishes
from schemas import CreateDish
from dish import create_dish

__all__ = ["init_seasons", "init_dishes"]


def init_seasons(session):
    logger.info("Initializing seasons")
    session.add(Season("Printemps", "🌱"))
    session.add(Season("Été", "☀"))
    session.add(Season("Automne", "🍂"))
    session.add(Season("Hiver", "🌨️"))
    session.commit()


def init_dishes(session):
    logger.info("Initializing dishes")
    create_dish(
        session, CreateDish(name="Sushis", from_restaurant=True, seasons=[1, 2, 3, 4])
    )
    create_dish(
        session, CreateDish(name="Pizza", from_restaurant=True, seasons=[1, 2, 3, 4])
    )
    create_dish(session, CreateDish(name="Pizza (maison)", seasons=[1, 2, 3, 4]))
    create_dish(
        session,
        CreateDish(
            name="Soupe poireaux / pommes de terre", seasons=[3, 4], vegetarian=True
        ),
    )
    create_dish(
        session, CreateDish(name="Tarte poireaux", seasons=[3, 4], vegetarian=True)
    )
    create_dish(session, CreateDish(name="Pâtes carbonara", seasons=[1, 2, 3, 4]))
    create_dish(session, CreateDish(name="Spaghetti bolognaise", seasons=[1, 2, 3, 4]))
    create_dish(
        session, CreateDish(name="Porc à la vietnamienne", seasons=[1, 2, 3, 4])
    )
    create_dish(
        session, CreateDish(name="Poulet champignons / moutarde", seasons=[1, 2, 3, 4])
    )
    create_dish(session, CreateDish(name="Croques monsieur", seasons=[1, 2, 3, 4]))
    create_dish(session, CreateDish(name="Apéro dînatoire", seasons=[1, 2, 3, 4]))
    create_dish(
        session,
        CreateDish(name="Tarte comté / tomates", seasons=[1, 2], vegetarian=True),
    )
    create_dish(session, CreateDish(name="Salade de riz", seasons=[1, 2]))
    create_dish(session, CreateDish(name="Salade de pâtes", seasons=[1, 2]))
    create_dish(session, CreateDish(name="Quiche lorraine", seasons=[1, 2, 3, 4]))
    create_dish(session, CreateDish(name="Poulet basquaise", seasons=[1, 2]))
    create_dish(session, CreateDish(name="Galettes", seasons=[1, 2, 3, 4]))
    create_dish(
        session,
        CreateDish(name="Curry patates douces, épinards et riz", seasons=[1, 3]),
    )
    create_dish(
        session,
        CreateDish(
            name="Boulettes d'agneau, ratatouille et semoule", seasons=[1, 2, 3, 4]
        ),
    )
    create_dish(session, CreateDish(name="Taboulé", seasons=[1, 2])),
    create_dish(
        session,
        CreateDish(name="Parmigianna (aubergines)", seasons=[1, 2], vegetarian=True),
    )
    create_dish(
        session,
        CreateDish(name="Burgers", seasons=[1, 2]),
    )
    session.commit()
