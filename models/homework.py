from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Homework(Base):
    __tablename__ = 'homework'

    id = Column(Integer, primary_key=True)  # ID домашнего задания
    lesson_id = Column(Integer, ForeignKey('schedule.id'), nullable=False)  # Привязка к уроку
    description = Column(String(1000), nullable=False)  # Текст домашнего задания
    due_date = Column(DateTime, nullable=False)  # Дата сдачи задания
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Время добавления задания