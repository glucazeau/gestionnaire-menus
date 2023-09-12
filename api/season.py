from sqlalchemy.orm import Session

from models import Season


def list_seasons(db: Session):
    return db.query(Season).all()


def get_season(date):
    return season
