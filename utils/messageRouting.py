import json

from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy import create_engine

from database.models.GroupUser import GroupUser
engine = create_engine('postgresql://postgres:postgres@localhost:5433/ChatSystem', echo=True)


#
# def messageRouter(clients, message,message_queue):
#     # Parse the message JSON
#     message_data = json.loads(message.decode())
#
#     # Get the receiver ID from the message
#     receiver_id = message_data['recipient_id']
#     # Check if the receiver ID is in the list of clients
#     if receiver_id in clients:
#         # Get the client socket for the receiver
#         receiver_socket = clients[receiver_id]
#         # Send the message to the client
#         receiver_socket.send(message)
#
#         # Print a confirmation message
#         print(f"Sent message to {receiver_id}")
#     else:
#         # Print an error message if the recipient ID is not found
#         print(f"Recipient {receiver_id} is offline. Queuing message.")
#         # Add the message to the recipient's message queue
#         if receiver_id not in message_queue:
#             message_queue[receiver_id] = []
#         message_queue[receiver_id].append(message.decode('utf-8'))


def Group_messageRouter(clients, message):
    # Parse the message JSON
    message_data = json.loads(message.decode())

    #Find this groupid in database if available fetch all the group member user_id
    user_id = get_users_in_group(message_data['group_id'],message_data['user_id'])
    print(user_id)

    # Check if the receiver ID is in the list of clients
    # if Group_id in clients:
    #     # Get the client socket for the receiver
    #     receiver_socket = clients[Group_id]
    #     # Send the message to the client
    #     receiver_socket.send(message)
    #
    #     # Print a confirmation message
    #     print(f"Sent message to {Group_id}")
    # else:
    #     # Print an error message if the recipient ID is not found
    #     print(f"Recipient {Group_id} Not Found.")


def get_users_in_group(group_id, user_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if the group_id and user_id exist in group_user table
    if session.query(exists().where(GroupUser.group_id == group_id and GroupUser.user_id == user_id)).scalar():
        # Fetch all user_id in the group for the given group_id
        users_in_group = session.query(GroupUser.user_id).filter(GroupUser.group_id == group_id).all()
        return [user_id for (user_id,) in users_in_group]

    return None