from datetime import datetime

from sqlalchemy.orm import sessionmaker

from database.models.GroupChat import GroupChat
from database.models.GroupUser import GroupUser
from database.models.Users import Users
from sqlalchemy import create_engine

def deliver_queued_messages_singleChat(client_socket, client_id, message_queue):
    # Check if there are any queued messages for the client
    if client_id in message_queue:
        # Send each queued message to the client socket
        for message in message_queue[client_id]:
            client_socket.send(message.encode('utf-8'))
        # Remove the client ID from the message queue
        del message_queue[client_id]

engine = create_engine('postgresql://postgres:postgres@localhost:5433/ChatSystem', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def get_messages_for_user_groupChat(user_id):
    try:
        # Get the user from the database using the provided user_id
        user = session.query(Users).filter_by(id=user_id).first()

        if not user:
            print(f"User {user_id} not found in the database.")
            return []

        current_time = datetime.now()

        # If the user is online, no need to fetch missed messages
        if user.status == "online":
            return []

        # If the user is offline, fetch messages between last_seen and current_time
        last_seen = user.status

        # If last_seen is None, set it to current_time to mark that the messages have been fetched
        if last_seen is None:
            last_seen = current_time

        # Fetch messages sent to groups the user is a part of between last_seen and current_time
        messages = session.query(GroupChat).filter(
            GroupChat.group_id.in_(
                session.query(GroupUser.group_id).filter(GroupUser.user_id == user_id)
            ),
            GroupChat.timestamp >= last_seen,
            GroupChat.timestamp <= current_time
        ).all()

        messages_json = []
        for message in messages:
            message_data = {
                "user_id": message.user_id,
                "group_id": message.group_id,
                "message": message.group_message
            }
            messages_json.append(message_data)



        # Update last_seen to the current time to mark that the messages have been fetched
        user.last_seen = current_time
        session.commit()

        return messages_json

    except Exception as e:
        session.rollback()
        print(f"Error fetching messages for User {user_id}: {e}")
        return []

    finally:
        session.close()
def update_user_status(user_id, status):
    try:
        # Update the status directly in the database using the update() method
        if status.lower() == "online":
            session.query(Users).filter_by(id=user_id).update({"status": "online"})
        elif status.lower() == "offline":
            session.query(Users).filter_by(id=user_id).update({"status": datetime.now() })
        else:
            print("Invalid status choice. Please provide 'online' or 'offline'.")
            return

        session.commit()
        print(f"User {user_id} status updated to '{status}'.")

    except Exception as e:
        session.rollback()
        print(f"Error updating status for User {user_id}: {e}")

    finally:
        session.close()
