from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy import create_engine
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Модель для учебных групп
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    schedules = relationship("Schedule", back_populates="group", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Group(name={self.name})>"

# Модель для расписания
class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    day = Column(String, nullable=False)
    time = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    teacher = Column(String)
    building = Column(String)
    floor = Column(String)
    room = Column(String)
    group = relationship("Group", back_populates="schedules")

    def __repr__(self):
        return f"<Schedule(day={self.day}, time={self.time}, subject={self.subject})>"

# Создание таблиц
def create_tables():
    Base.metadata.create_all(engine)

# Функция для получения сессии базы данных
def get_db_session():
    return SessionLocal()