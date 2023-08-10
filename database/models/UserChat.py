from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


from database.models.Users import Users

Base = declarative_base()
class UserChat(Base):
    __tablename__ = 'user_chat'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.phone_number))
    reciever_id = Column(Integer)
    user_message = Column(String)
    timestamp = Column(DateTime, server_default=text('NOW()'))



    user = relationship(Users)
