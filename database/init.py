from sqlalchemy import create_engine
from models.Users import Users

engine = create_engine('postgresql://postgres:postgres@localhost:5433/ChatSystem', echo=True)


Users.metadata.create_all(engine)
