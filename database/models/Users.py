from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(String)
    status = Column(String)

