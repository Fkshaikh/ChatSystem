from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database.models.Groups import Groups
from database.models.Users import Users

Base = declarative_base()


class GroupUser(Base):
    __tablename__ = 'group_user'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey(Groups.id))
    user_id = Column(Integer, ForeignKey(Users.id))

    group = relationship(Groups)
    user = relationship(Users)
