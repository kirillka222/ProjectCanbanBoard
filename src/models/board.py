from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from src.core.db import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_name = Column(String, nullable=False)
    description = Column(String)
    datetime = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="boards")  # 1 польз много досок
    columns = relationship("Columns", back_populates="board")  # 1 доска много колонок
