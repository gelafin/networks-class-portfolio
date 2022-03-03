# Author: Mark Mendez
# Date: 02/22/2022
# used starter code and concepts from "Computer Networking: A Top-Down Approach" by James F. Kurose and Keith Ross

from socket import *
from socket_constants import *
from game_constants import *
from game_helpers import RPSGameManager


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

    # Accept only one connection.
    # This is where a forever loop would start if accepting many connections.
    connection_socket, client_address = server_socket.accept()

    # Print this socket's configuration data
    print(f'Connected at {SERVER_NAME}:{SERVER_PORT}. Type {QUIT_MESSAGE} to quit.\n')

    # Instantiate the game manager, which tracks state
    game_manager = RPSGameManager()

    # Print a server-specific notice
    print('You are player 2. Waiting for player 1 to select a stage and a first move...\n')

    # Interact with the new connection
    game_manager.play_game(connection_socket)

    # Close the connection
    connection_socket.close()

    print('\nConnection closed.')


if __name__ == '__main__':
    main()
