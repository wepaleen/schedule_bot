from tokenize import group

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from config import DATABASE_URL

engine = create_engine(DATABASE_URL,
                       pool_size=10,
                       max_overflow=20,
                       pool_timeout=30,
                       pool_recycle=1800
                       )
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


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
    group = relationship('Group')

Base.metadata.create_all(engine)