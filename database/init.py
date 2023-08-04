from sqlalchemy import create_engine

from database.models.GroupUser import GroupUser
from database.models.Users import Users
from database.models.Groups import Groups
from database.models.GroupChat import GroupChat


engine = create_engine('postgresql://postgres:postgres@localhost:5433/ChatSystem', echo=True)



Groups.metadata.create_all(engine)

Users.metadata.create_all(engine)

GroupUser.metadata.create_all(engine)

GroupChat.metadata.create_all(engine)

