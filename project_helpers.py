# Author: Mark Mendez
# Date: 02/23/2022

from socket import socket
from project_constants import *


def handle_new_message(incoming_message: str, connection_socket: socket):
    """
    Displays the received message, prompts for a reply message,
    and sends the reply message through the given socket.
    :param incoming_message: message received from the other host
    :param connection_socket: socket object representing the connection
    """
    print(f'Received: {incoming_message}')

    # Get a message to send to the client
    res_message = input('Type response... ')

    print(f'Sending response: {res_message}')

    # Send the response message
    # TODO: make a helper capable of chunking responses
    connection_socket.send(res_message.encode())


def receive_next_chunk(connection_socket: socket) -> dict:
    """
    Receives the next chunk of data from the given socket
    and parses the data according to the made-up GELA372 protocol.
    In GELA372, the first byte of every packet is an ID number,
    and a receiver accumulates chunks until detecting a change in ID number.
    :param connection_socket: socket object representing the connection
    :return: chunk data in the form
             {'id': str, 'payload': str}
    """
    # Receive a chunk of raw byte message and decode it into a string
    req_message_chunk = connection_socket.recv(BUFFER_SIZE).decode()

    # Check message ID using the GELA372 protocol.
    chunk_id = req_message_chunk[0:1]
    chunk_payload = req_message_chunk[1:len(req_message_chunk)]

    # Wrap up the extracted data, nice and neat
    chunk_data_out = {
        'id': chunk_id,
        'payload': chunk_payload
    }

    return chunk_data_out


def handle_new_connection(connection_socket: socket):
    """
    Interacts with another until receiving a quit message from the other host.
    Starts interaction by receiving.
    :param connection_socket: socket object representing the connection
    """
    # Print this socket's configuration data
    print(f'Connected at {SERVER_NAME}:{SERVER_PORT}. Type {QUIT_MESSAGE} to quit.')

    # Initialize the first message's data with the first chunk's data
    chunk_data = receive_next_chunk(connection_socket)
    chunk_id = chunk_data['id']
    chunk_payload = chunk_data['payload']
    incoming_message_id = chunk_id
    incoming_message_payload = chunk_payload

    # Receive and reply to messages in chunks from client until a message matches the quit message
    while incoming_message_payload != QUIT_MESSAGE:
        # If this chunk is the first of a new message, process the message that just finished transmitting.
        # The request message payload is now completely received.
        if chunk_id != incoming_message_id and len(incoming_message_payload) > 0:
            # Check for quit message
            if incoming_message_payload == QUIT_MESSAGE:
                return

            handle_new_message(incoming_message_payload, connection_socket)

            # Reset to track the new message
            incoming_message_id = chunk_id
            incoming_message_payload = ''

        # Receive a chunk of data from the other host
        chunk_data = receive_next_chunk(connection_socket)
        chunk_id = chunk_data['id']
        chunk_payload = chunk_data['payload']

        # Add this chunk's payload to the message text
        incoming_message_payload += chunk_payload
