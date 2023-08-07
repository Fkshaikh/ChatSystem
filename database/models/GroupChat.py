from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from database.models.Groups import Groups
from database.models.Users import Users

Base = declarative_base()
class GroupChat(Base):
    __tablename__ = 'group_chat'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.id))
    group_id = Column(Integer, ForeignKey(Groups.id))
    group_message = Column(String)
    timestamp = Column(DateTime, server_default=text('NOW()'))


    group = relationship(Groups)
    user = relationship(Users)
