import json
import socket
import threading
import time

# Define the host and port for the server
HOST = 'localhost'
PORT = 8001

user_id = "2"

def auth():
    # Create a socket object and connect it to the server


    token = "abcdefg"
    auth_token = {"user_id":user_id,"token":token}

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((HOST, PORT))
    # Send the authentication token to the server
    client_socket.send(json.dumps(auth_token).encode('utf-8'))

    # Wait for a response from the server
    response = client_socket.recv(1024).decode('utf-8')
    response_data = json.loads(response)

    # Check if the authentication was successful
    if "error" in response_data:
        print(f"Authentication failed: {response_data['error']}")
        return False
    else:
        print("Authentication successful.")
        # Start a new thread to receive messages from the server
        receive_messages()
        return client_socket

def receive_messages():
    """
    Receive messages from the server and print them to the console.
    """
    while True:
        try:
            # Receive a message from the server
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            # If there was an error, exit the loop
            break

def send_messages(client_socket):
    """
    Get input from the user and send messages to the server.
    """
    while True:
        try:
            # Get input from the user
            message_body = input("Enter Message:")
            group_id = input("Enter Group Id:")

            # Create a message payload as a JSON string
            payload = {"message_body": message_body, "user_id": user_id,"group_id":group_id}
            payload = json.dumps(payload)

            # Send the message to the server
            client_socket.send(payload.encode('utf-8'))

            print("Message sent.")
        except:
            # If there was an error, exit the loop
            print("Error sending message.")
            break

# Authenticate the user and start the message receiving thread
client_socket = auth()
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

if client_socket:
    # Start a new thread to send messages to the server
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()
else:
    print("Authentication failed.")


