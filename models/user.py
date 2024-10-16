from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)  # ID пользователя (Telegram user_id)
    username = Column(String(255), nullable=True)  # Имя пользователя (Telegram username)
    full_name = Column(String(255), nullable=True)  # Полное имя пользователя
    role = Column(String(50), nullable=False, default='student')  # Роль пользователя (student, teacher, admin)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Время регистрации пользователя