from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL, echo=True)
session = sessionmaker(engine)


class Base(DeclarativeBase):

    pass


def get_db():
    db = session()
    try:
        return db
    finally:
        db.close()
