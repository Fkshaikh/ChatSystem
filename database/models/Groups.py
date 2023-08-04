from sqlalchemy import UUID, text

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Groups(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    group_id = Column(UUID(as_uuid=True), server_default=text('uuid_generate_v4()'), unique=True)
    group_name = Column(String)