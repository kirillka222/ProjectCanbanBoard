from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from src.core.db import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    column_id = Column(Integer, ForeignKey("columns.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    deadline = Column(DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=3))

    column = relationship("Columns", back_populates="tasks") # 1 zadasha - 1 kolonka







