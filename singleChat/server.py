import json
import socket
import threading
from utils.messageRouting import messageRouter
from utils.auth import verify_auth
from utils.queue_Message import deliver_queued_messages_singleChat
# Define the host and port for the server
HOST = 'localhost'
PORT = 8000

# Create a socket object and bind it to the host and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

clients = {}  # twick required ! will have to use in memory database so it can become scalable (use redis)
message_queue = {} #twick required !will have to use in queuing database


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
        print(f"User {message_data['client_id']} authenticated.")

        response = {"status": "success", "message": "Authentication successful."}

        response_json = json.dumps(response)

        client_socket.send(response_json.encode('utf-8'))

        clients[message_data.get('client_id')] = client_socket

        # Deliver any queued messages to the client
        deliver_queued_messages_singleChat(client_socket, message_data['client_id'], message_queue)

    else:
        print(f"User {message_data['client_id']} authentication failed.")
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

        messageRouter(clients, message,message_queue)
        print(f"Received message from {message_data['client_id']}: {message}")

    # Close the client socket when the connection is closed
    print(f"User {message_data['client_id']} disconnected.")
    client_socket.close()
    # Remove the client ID from the clients dictionary
    if message_data['client_id'] in clients:
        del clients[message_data['client_id']]


# Main loop to handle incoming connections
while True:
    # Accept a new client connection
    client_socket, addr = server_socket.accept()

    # Start a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
