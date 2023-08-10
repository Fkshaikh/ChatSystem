from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models.GroupUser import GroupUser
from database.models.UserChat import UserChat
from database.models.Users import Users
from database.models.Groups import Groups
from database.models.GroupChat import GroupChat

# Create the database engine
engine = create_engine('postgresql://postgres:postgres@localhost:5433/ChatSystem', echo=True)

# Create all tables
Groups.metadata.create_all(engine)
Users.metadata.create_all(engine)
GroupUser.metadata.create_all(engine)
GroupChat.metadata.create_all(engine)
UserChat.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Seed the data
try:
    # Create Users
    user1 = Users(phone_number=1234567890, name='John Doe')
    user2 = Users(phone_number=7865432, name='Saif Doe')
    session.add_all([user1, user2])
    session.commit()

    # Create Groups
    group1 = Groups(group_name='Sample Group')
    session.add(group1)
    session.commit()

    # Create GroupUser
    group_user1 = GroupUser(group_id=1, user_id=1)
    group_user2 = GroupUser(group_id=1, user_id=2)
    session.add_all([group_user1, group_user2])
    session.commit()

    # Create GroupChat
    group_chat1 = GroupChat(user_id=1, group_id=1, group_message='Hello everyone!')
    session.add(group_chat1)
    session.commit()

    print("Data seeding successful.")

except Exception as e:
    session.rollback()
    print("Error occurred while seeding data:", e)

finally:
    session.close()
