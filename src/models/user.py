from sqlalchemy import Column, Integer, String, Boolean
from src.core.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    email = Column(String)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)

    boards = relationship("Board", back_populates="owner")


Base = declarative_base()
