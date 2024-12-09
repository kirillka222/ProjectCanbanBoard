from sqlalchemy import Column, Integer, String, ForeignKey
from src.core.db import Base
from sqlalchemy.orm import relationship


class Columns(Base):
    __tablename__ = "columns"
    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)
    name = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="column") # одна колонка много задач
    board = relationship("Board", back_populates="columns") # одна колонка одна доска






