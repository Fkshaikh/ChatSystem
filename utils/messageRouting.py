import heapq
import json
import time

from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy import create_engine

from database.models.GroupChat import GroupChat
from database.models.GroupUser import GroupUser

engine = create_engine('postgresql://postgres:postgres@localhost:5433/ChatSystem', echo=True)



def messageRouter(clients, message,message_queue):
    # Parse the message JSON
    message_data = json.loads(message.decode())

    # Get the receiver ID from the message
    receiver_id = message_data['recipient_id']

    # Check if the receiver ID is in the list of clients
    if receiver_id in clients:

        # Get the client socket for the receiver
        receiver_socket = clients[receiver_id]

        # Send the message to the client
        receiver_socket.send(message)

        # Print a confirmation message
        print(f"Sent message to {receiver_id}")
    else:

        # Print an error message if the recipient ID is not found
        print(f"Recipient {receiver_id} is offline. Queuing message.")

        # Add the message to the recipient's message queue
        if receiver_id not in message_queue:
            message_queue[receiver_id] = []

        message_queue[receiver_id].append(message.decode('utf-8'))



# Create a priority queue to track the expiration times of cached items
expiration_queue = []

# Set the time-to-live for cached items (in seconds)
CACHE_TTL = 3600  # Example: 1 hour

group_cache = {}  # twick Required ! need Cache Memory


def evict_expired_cache_items():
    # Function to evict expired cache items
    current_time = time.time()
    while expiration_queue and expiration_queue[0][0] <= current_time:
        _, group_id = heapq.heappop(expiration_queue)
        if group_id in group_cache:
            del group_cache[group_id]

def Group_messageRouter(clients, message):

    # Evict expired cache items before processing the message
    evict_expired_cache_items()

    # Parse the message JSON
    message_data = json.loads(message.decode())

    group_id = message_data['group_id']
    sender_socket = message_data['user_id']

    # Find this groupid in the cache first
    if group_id in group_cache:
        timestamp, user_ids = group_cache[group_id]

    else:

        # Fetch all the group member user_ids from the database
        user_ids = get_users_in_group(group_id, sender_socket)

        # Store the group details in the cache with the current timestamp
        timestamp = time.time()
        group_cache[group_id] = (timestamp, user_ids)

        # Add the expiration time to the priority queue
        heapq.heappush(expiration_queue, (timestamp + CACHE_TTL, group_id))


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

    # Create a reverse mapping of clients dictionary
    user_id_to_socket = {str(client_user_id): client_socket for client_user_id, client_socket in clients.items()}

    # Find the online users using the reverse mapping
    online_users = [user_id_to_socket[str(user_id)] for user_id in user_ids if str(user_id) in user_id_to_socket]

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