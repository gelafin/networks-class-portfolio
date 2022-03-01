# Author: Mark Mendez
# Date: 02/22/2022
# used starter code and concepts from "Computer Networking: A Top-Down Approach" by James F. Kurose and Keith Ross

from socket import *
from project_constants import *
from project_helpers import play_game


def main():
    """Be a server"""
    print('starting server')

    # Create a server socket,
    # Using default address family (SOCK_STREAM means to use TCP)
    server_socket = socket(family=AF_INET, type=SOCK_STREAM)

    # Listen for connections
    server_socket.bind(('', SERVER_PORT))
    server_socket.listen(1)  # allow max of 1 queued connection
    print('listening for connection requests')

    # Accept and handle requests
    while True:
        # Accept a new connection
        connection_socket, client_address = server_socket.accept()

        # Print this socket's configuration data
        print(f'Connected at {SERVER_NAME}:{SERVER_PORT}. Type {QUIT_MESSAGE} to quit.')

        # Print a server-specific notice
        print('Waiting for player 1 to select a stage...')

        # Interact with the new connection
        play_game(connection_socket)

        # Close the connection
        connection_socket.close()

        print('connection closed. Listening for a new connection request.')


if __name__ == '__main__':
    main()
