# Author: Mark Mendez
# Date: 02/22/2022
# used starter code and concepts from "Computer Networking: A Top-Down Approach" by James F. Kurose and Keith Ross

from socket import *
from project_constants import *
from project_helpers import *


def main():
    """Be a client"""
    # Choose a message to send to the other host
    outgoing_message = input('Type the first message to start a connection... ')

    # Create a client socket,
    # using default address family (SOCK_STREAM means to use TCP)
    client_socket = socket(family=AF_INET, type=SOCK_STREAM)

    # Connect to the server specified above
    client_socket.connect((SERVER_NAME, SERVER_PORT))

    incoming_message = ''
    while incoming_message != QUIT_MESSAGE and outgoing_message != QUIT_MESSAGE:
        # Send message to server
        print(f'Sending first message:\n{outgoing_message}')
        send_message(outgoing_message, client_socket)

        # Interact with the server
        handle_new_connection(client_socket)

    # Close socket connection
    client_socket.close()


if __name__ == '__main__':
    main()
