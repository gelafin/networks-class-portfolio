# Author: Mark Mendez
# Date: 02/22/2022
# used starter code and concepts from "Computer Networking: A Top-Down Approach" by James F. Kurose and Keith Ross

from socket import *
from socket_constants import *
from game_constants import *
from socket_helpers import send_message
from game_helpers import RPSGameManager


def main():
    """Be a client"""
    # Create a client socket,
    # using default address family (SOCK_STREAM means to use TCP)
    client_socket = socket(family=AF_INET, type=SOCK_STREAM)

    # Connect to the server specified above
    client_socket.connect((SERVER_NAME, SERVER_PORT))

    # Print this socket's configuration data
    print(f'Connected at {SERVER_NAME}:{SERVER_PORT}. Type {QUIT_MESSAGE} to quit.')

    # Instantiate the game manager, which tracks state
    game_manager = RPSGameManager()

    # Select a stage
    stage_selection = input(STAGE_CHOICE_PROMPT)
    game_manager.set_stage(stage_selection)

    # Start the game by taking the first turn
    first_move = game_manager.prompt_next_move()
    game_manager.set_player_move('1', first_move)
    outgoing_message = game_manager.encode_state()
    send_message(outgoing_message, client_socket)

    # Interact with the server until sending or receiving a quit message
    game_manager.play_game(client_socket)

    # Close socket connection
    client_socket.close()


if __name__ == '__main__':
    main()
