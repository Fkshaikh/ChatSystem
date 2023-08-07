import json

from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy import create_engine

from database.models.GroupChat import GroupChat
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

    group_id = message_data['group_id']
    sender_socket = message_data['user_id']

    # Find this groupid in database if available fetch all the group member user_id
    user_ids = get_users_in_group(group_id, sender_socket)

    if user_ids:
        #find users online in the group
        online_users = get_online_users(user_ids, clients)

        # Send the message to online users
        send_message_to_group_members(online_users, message)

        # Save the message to the database
        save_message_to_database(message_data['message_body'], sender_socket, int(group_id))

        # Print a confirmation message
        print(f"Sent message to {group_id}")

    else:
        # Send the message to the client
        sender_socket.send("Group Not Found".encode())


def get_users_in_group(group_id, user_id):

    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if the group_id and user_id exist in group_user table
    if session.query(exists().where(GroupUser.group_id == group_id and GroupUser.user_id == user_id)).scalar():

        # Fetch all user_id in the group for the given group_id
        users_in_group = session.query(GroupUser.user_id).filter(GroupUser.group_id == group_id).all()

        return [user_id for (user_id,) in users_in_group]

    return False



def get_online_users(user_ids, clients):
    # Function to check which user_ids are online from the list of user_ids
    online_users = []
    for user_id in user_ids:
        user_id = str(user_id)
        for client_user_id, client_socket in clients.items():
            if client_user_id == user_id:
                online_users.append(client_socket)
                break
    return online_users


def send_message_to_group_members(user_sockets, message):
    # Function to send the message to a list of user_sockets
    for user_socket in user_sockets:
        user_socket.sendall(message)

def save_message_to_database(message, sender_id, group_id):

    Session = sessionmaker(bind=engine)
    session = Session()

    group_chat_message = GroupChat(group_message=message, user_id=sender_id, group_id=group_id)

    session.add(group_chat_message)
    session.commit()