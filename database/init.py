from sqlalchemy import create_engine
from models.Users import Users
from models.Groups import Groups
from models.GroupUser import GroupUser
from models.GroupChat import GroupChat


engine = create_engine('postgresql://postgres:postgres@localhost:5433/ChatSystem', echo=True)



Groups.metadata.create_all(engine)

Users.metadata.create_all(engine)

GroupUser.metadata.create_all(engine)

GroupChat.metadata.create_all(engine)

