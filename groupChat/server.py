import json
import socket
import threading

from utils.messageRouting import  Group_messageRouter
from utils.auth import verify_auth

from utils.queue_Message import get_messages_for_user_groupChat, update_user_status

# Define the host and port for the server
HOST = 'localhost'
PORT = 8001

# Create a socket object and bind it to the host and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

clients = {}  # twick required ! will have to use in memory database so it can become scalable (use redis)




# Define a function to handle client connections
def handle_client(client_socket):


    # Wait for authentication message from the client
    message = client_socket.recv(1024)
    if not message:
        client_socket.close()
        return

    # Verify the authentication token in the message
    try:
        message_data = json.loads(message.decode('utf-8'))
    except ValueError:
        client_socket.close()
        return

    if verify_auth(message_data):
        authenticated_user_id = message_data['user_id']

        print(f"User {authenticated_user_id} authenticated.")

        response = {"status": "success", "message": "Authentication successful."}

        response_json = json.dumps(response)

        client_socket.send(response_json.encode('utf-8'))

        clients[authenticated_user_id] = client_socket


        #send the pending messages to the user
        pending_messages = get_messages_for_user_groupChat(authenticated_user_id)

        # Update user status in database
        update_user_status(authenticated_user_id, 'Online')

        #Send pending message to client
        for message_data in pending_messages:
            message_json = json.dumps(message_data)
            client_socket.sendall(message_json.encode('utf-8'))

    else:
        print(f"User {message_data['user_id']} authentication failed.")
        response = {"status": "error", "message": "Authentication failed."}
        response_json = json.dumps(response)
        client_socket.send(response_json.encode('utf-8'))
        client_socket.close()
        return

    # Receive messages from the client
    while True:
        message = client_socket.recv(1024)
        if not message:
            break

        Group_messageRouter(clients, message)
        print(f"Received message from {authenticated_user_id}: {message}")

    # Close the client socket when the connection is closed
    print(f"User {authenticated_user_id} disconnected.")

    # update user status in database
    update_user_status(authenticated_user_id, 'offline')
    client_socket.close()

    # Remove the client ID from the clients dictionary
    if message_data['user_id'] in clients:
        del clients[authenticated_user_id]


# Main loop to handle incoming connections
while True:
    # Accept a new client connection
    client_socket, addr = server_socket.accept()

    # Start a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
