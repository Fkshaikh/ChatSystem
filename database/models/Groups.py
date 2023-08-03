
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Groups(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    group_name = Column(String)