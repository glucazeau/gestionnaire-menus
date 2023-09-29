from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, MappedAsDataclass, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite:///./menus.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(MappedAsDataclass, DeclarativeBase):
    pass
