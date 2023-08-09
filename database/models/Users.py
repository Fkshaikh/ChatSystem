from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID

Base =declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), server_default=text('uuid_generate_v4()'), unique=True)
    phone_number = Column(Integer, unique=True)
    name = Column(String)
    status = Column(String)