# Author: Mark Mendez
# Date: 02/22/2022
# used starter code and concepts from "Computer Networking: A Top-Down Approach" by James F. Kurose and Keith Ross

from socket import *
from project_constants import *
from project_helpers import play_game, send_message, prompt_next_move


def main():
    """Be a client"""
    # Create a client socket,
    # using default address family (SOCK_STREAM means to use TCP)
    client_socket = socket(family=AF_INET, type=SOCK_STREAM)

    # Connect to the server specified above
    client_socket.connect((SERVER_NAME, SERVER_PORT))

    # Print this socket's configuration data
    print(f'Connected at {SERVER_NAME}:{SERVER_PORT}. Type {QUIT_MESSAGE} to quit.')

    # Select a stage
    stage_selection_message = input(STAGE_CHOICE_PROMPT)

    # Communicate stage selection to the other player
    send_message(stage_selection_message, client_socket)

    # Start the game by taking the first turn
    first_move = prompt_next_move()
    send_message(first_move, client_socket)

    # Interact with the server until sending or receiving a quit message
    play_game(client_socket)

    # Close socket connection
    client_socket.close()


if __name__ == '__main__':
    main()
