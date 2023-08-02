import json

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