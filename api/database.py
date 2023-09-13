from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import MappedAsDataclass, Session, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite:///./menus.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Base(MappedAsDataclass, DeclarativeBase):
    pass