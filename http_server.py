# Author: Mark Mendez
# Date: 02/22/2022
# used starter code and concepts from "Computer Networking: A Top-Down Approach" by James F. Kurose and Keith Ross

from socket import *
from project_constants import *
from project_helpers import handle_new_connection


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

        # Interact with the new connection
        handle_new_connection(connection_socket)

        # Close the connection
        connection_socket.close()


if __name__ == '__main__':
    main()
