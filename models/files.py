from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)  # ID файла
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ID пользователя, который загрузил файл
    homework_id = Column(Integer, ForeignKey('homework.id'), nullable=True)  # ID домашнего задания, к которому привязан файл
    file_name = Column(String(255), nullable=False)  # Имя файла
    file_path = Column(String(255), nullable=False)  # Путь к файлу на сервере
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())  # Время загрузки файла