# Author: Mark Mendez
# Date: 02/22/2022
# used starter code and concepts from "Computer Networking: A Top-Down Approach" by James F. Kurose and Keith Ross

from socket import *
from socket_constants import *
from game_constants import *
from game_helpers import RPSGameManager
from generic_utils import get_validated_input


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
    all_stages = [stage for stage in STAGES]
    validation_error_message = 'If you really want more stages, fork the repo.'
    stage_selection = get_validated_input(STAGE_CHOICE_PROMPT, all_stages, validation_error_message, True)
    game_manager.set_stage(stage_selection)

    # Start the game by taking the first turn
    game_manager.play_next_move()
    game_manager.send_state_to_opponent(client_socket)

    # Edge case: if local player's initial move is quit message, skip remaining interaction
    if game_manager.get_local_player_move() != QUIT_MESSAGE:
        # Tell local player to wait for opponent
        print(WAITING_FOR_OPPONENT_MESSAGE)

        # Interact with the server until sending or receiving a quit message
        game_manager.play_game(client_socket)

    else:
        print('No contest.')

    # Close socket connection
    client_socket.close()

    print('\nConnection closed.')


if __name__ == '__main__':
    main()
