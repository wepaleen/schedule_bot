from sqlalchemy import Column, Integer, String, Time, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True)  # ID расписания
    lesson_name = Column(String(255), nullable=False)  # Название урока
    day_of_week = Column(String(50), nullable=False)  # День недели (например, 'Monday')
    start_time = Column(Time, nullable=False)  # Время начала урока
    end_time = Column(Time, nullable=False)  # Время окончания урока
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Время добавления записи