"""Подключение к базе данных"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import db_connection
from models.homework import Homework
from models.user import User

# Настраиваем подключение к базе данных
engine = create_engine(db_connection)
Session = sessionmaker(bind=engine)
session = Session()

# Пример: добавление нового пользователя
new_user = User(id=123456789, username='ruslan', full_name='Руслан Иванов')
session.add(new_user)
session.commit()

# Пример: добавление домашнего задания
new_homework = Homework(lesson_id=1, description='Сделать упражнение 5', due_date='2024-10-15')
session.add(new_homework)
session.commit()

# Пример: получение всех домашних заданий для конкретного урока
homeworks = session.query(Homework).filter_by(lesson_id=1).all()
for homework in homeworks:
    print(homework.description)