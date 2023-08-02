
def deliver_queued_messages(client_socket, client_id, message_queue):
    # Check if there are any queued messages for the client
    if client_id in message_queue:
        # Send each queued message to the client socket
        for message in message_queue[client_id]:
            client_socket.send(message.encode('utf-8'))
        # Remove the client ID from the message queue
        del message_queue[client_id]
