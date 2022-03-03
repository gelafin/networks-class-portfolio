# Author: Mark Mendez
# Date: 03/01/2022

import copy
import json
import enum
import random
from typing import Tuple, List
from socket_helpers import *
from game_constants import *
from generic_utils import get_validated_input


class EndGameCode(enum.Enum):
    """
    Defines choices for end-game codes
    """
    CONTINUE = enum.auto()
    LOCAL_PLAYER_QUITS = enum.auto()
    OPPONENT_QUITS = enum.auto()


class RPSGameManager:
    """
    Helper class for Super Rock-Paper-Scissors.
    Tracks local state and sends socket messages to align state between players.
    """
    def __init__(self):
        """
        Initializes local game state
        """
        _INITIAL_PLAYER_STATE = {
            'score': 0,
            'move_choices': None,
            'current_move': ''  # one of the R/P/S options
        }

        self._INITIAL_STAGE = ''

        self.state = {
            'whose_turn': PLAYER_1,  # 1 or 2 (player 1 or player 2)
            'round_winner': '',
            'stage': self._INITIAL_STAGE,  # one of the constant STAGE options
            'player': {  # language limitation: have to hard-code player strings for dict keys
                '1': copy.deepcopy(_INITIAL_PLAYER_STATE),
                '2': copy.deepcopy(_INITIAL_PLAYER_STATE)
            }
        }

    def handle_endgame(self):
        """
        Shows final score
        """
        print('\n***Final scores***')
        self.show_scores()

    def set_player_move_options(self, player, updated_options: dict):
        """
        :param player:
        :param updated_options:
        """
        self.state['player'][player]['move_choices'] = updated_options

    def print_stage_info(self):
        """
        Prints info about the current stage
        """
        stage = self.state['stage']
        initial_move_options = STAGES[stage]

        print(f'Playing on stage {stage}')
        print(f'On {stage}, you both start with the following move options:')
        print(initial_move_options)
        print('')  # newline to separate this section

    def set_stage(self, stage: str):
        """
        Updates player 2 to use the stage selected by player 1,
        and notifies player 2 of stage conditions.
        :param stage: message received from player 1
        """
        initial_move_options = STAGES[stage]

        # Set the stage
        self.state['stage'] = stage

        # Print info about the new stage
        self.print_stage_info()

        # Initialize player move choices according to the stage
        self.set_player_move_options(PLAYER_1, copy.deepcopy(initial_move_options))
        self.set_player_move_options(PLAYER_2, copy.deepcopy(initial_move_options))

    def record_player_move(self, player: str, move: str):
        """
        Sets the move of the given player in game state
        :param player: 1 or 2 (player 1 or player 2)
        :param move: R, P, or S
        """
        # Record which move was taken
        self.state['player'][player]['current_move'] = move

        # Subtract this move from the player's remaining options
        if move != QUIT_MESSAGE:
            self.state['player'][player]['move_choices'][move] -= 1

    @staticmethod
    def decode_state(state_string: str) -> dict:
        """
        Reads the game's state from a given string.
        Assumes state_string is valid.
        :param state_string: string containing game state, encoded in format used by self.encode_state
        :return: dict describing the game's state, in the format used by encode_state()
        """
        return json.loads(state_string)

    def encode_state(self) -> str:
        """
        Creates a string holding the game's state.
        :return string version of game state
        """
        return json.dumps(self.state)

    def get_player_move_options(self, player: str) -> dict:
        """
        Returns the dict of move options for a given player
        :param player: 1 for player 1, or 2 for player 2
        :return: move options for the given player
        """
        return self.state['player'][player]['move_choices']

    def get_all_valid_moves(self, player: str) -> List[str]:
        """
        Returns a list of all valid move options, including quit option
        :return: list of all valid move options, including quit option
        """
        valid_moves = []

        # List all moves of which player has > 0 remaining
        for move in self.get_player_move_options(player):
            if self.state['player'][player]['move_choices'][move] > 0:
                valid_moves.append(move)

        # Allow quit message to be selected
        valid_moves.append(QUIT_MESSAGE_PRINTABLE)

        return valid_moves

    def play_next_move(self) -> str:
        """
        Shows players' remaining move options and prompts current player for a new move.
        Sets current player's move selection.
        """
        # Show both players' remaining move options
        local_player = self.get_local_player()
        local_player_move_options = self.get_player_move_options(local_player)
        print(f'Your remaining options:{local_player_move_options}')

        # Your turn--what's your move?
        valid_moves = self.get_all_valid_moves(local_player)
        validation_error_message = 'No fancy stuff in this game. You have to win using the power of prediction!'
        move_selection = get_validated_input(TURN_PROMPT, valid_moves, validation_error_message, True)

        # Record the move selection
        self.record_player_move(self.state['whose_turn'], move_selection)

        return move_selection

    def get_local_player_move(self) -> str:
        """
        Returns the most recent move chosen by the local player
        :return: local player's most recent move; R, P, or S
        """
        local_player = self.get_local_player()

        local_player_move = self.state['player'][local_player]['current_move']

        return local_player_move

    def get_local_player(self) -> str:
        """
        Returns the local player's constant descriptor
        :return: the local player's constant descriptor
        """
        return self.state['whose_turn']

    def get_opponent(self) -> str:
        """
        Returns the opponent's constant descriptor
        :return: the opponent's constant descriptor
        """
        opponent = None

        if self.state['whose_turn'] == PLAYER_2:
            opponent = PLAYER_1
        elif self.state['whose_turn'] == PLAYER_1:
            opponent = PLAYER_2

        return opponent

    def get_opponent_move(self) -> str:
        """
        Returns the most recent move chosen by the opponent of the local player
        :return: opponent's most recent move; R, P, or S
        """
        opponent = self.get_opponent()

        opponent_move = self.state['player'][opponent]['current_move']

        return opponent_move

    def change_turn(self):
        """
        Changes who the current player is.
        In this game, both players take their turn at the same time,
        but they are processed one at a time.
        This method helps keep track of which player is being processed.
        """
        if self.state['whose_turn'] == PLAYER_2:
            self.state['whose_turn'] = PLAYER_1
        elif self.state['whose_turn'] == PLAYER_1:
            self.state['whose_turn'] = PLAYER_2

    def award_round_winner(self, winner: str):
        """
        Sets round winner in state and updates score
        :param winner: player who won
        """
        # Track round winner
        self.state['round_winner'] = winner

        # Increase score of round winner, if not a tie
        if winner != TIE:
            self.state['player'][winner]['score'] += 1

    def calculate_round_result(self):
        """
        Calculates the result of a completed round.
        Sets round_winner in state.
        """
        local_move = self.get_local_player_move()
        opponent_move = self.get_opponent_move()

        # Check if local player won
        if MOVE_PRIORITY[local_move] == opponent_move:
            winner = self.get_local_player()

        # Check if opponent won
        elif MOVE_PRIORITY[opponent_move] == local_move:
            winner = self.get_opponent()

        # This round was a tie
        else:
            winner = TIE

        # Update state
        self.award_round_winner(winner)

    def get_round_winner(self) -> str:
        """
        Returns the most recent round's winner
        :return: the most recent round's winner,
                 which could be either player, or TIE
        """
        return self.state['round_winner']

    def get_scores(self) -> Tuple:
        """
        Returns scores of both players
        :return: Tuple of scores.
                 First score is local player's,
                 second score is opponent's
        """
        local_player_score = self.state['player'][self.get_local_player()]['score']
        opponent_score = self.state['player'][self.get_opponent()]['score']

        return local_player_score, opponent_score

    def show_scores(self):
        """
        Prints current scores for both players
        """
        local_player_score, opponent_score = self.get_scores()
        print(f'Your score: {local_player_score}')
        print(f'Opponent score: {opponent_score}')

    def count_remaining_move_options(self, player: str) -> int:
        """
        Totals the remaining move options for a given player
        :param player:
        :return: sum of all remaining move options for a given player
        """
        return sum(self.state['player'][player]['move_choices'].values())

    def regenerate_random_option(self, player: str):
        """
        Regenerates a random one of the given player's options
        """
        random_option = random.choice(ALL_MOVES)
        self.state['player'][player]['move_choices'][random_option] += REGEN_QUANTITY_EACH

    def handle_end_of_round(self):
        """
        Calculates and displays result of one round, after both players have taken their turn
        """
        # Award point and record round winner
        self.calculate_round_result()

        # Display results
        # Show opponent's move choice
        print(f'{REPLY_LINE_PREFIX}{self.get_opponent_move()}')

        # Print a newline to separate this summary section
        print('')

        # Show round winner
        winner = self.get_round_winner()
        if winner != TIE:
            print(f'Player {winner} wins this round!')
        else:
            print('This round was a tie!')

        # Show current score
        self.show_scores()

        # Print a newline at the end of the summary section
        print('')

        # Regenerate move choices if remaining move options have dwindled too much,
        # so the game can continue until a player quits
        local_player = self.get_local_player()
        if self.count_remaining_move_options(local_player) < REGEN_THRESHOLD:
            for _ in range(REGEN_ITERATIONS):
                self.regenerate_random_option(local_player)

            print('\nYou randomly regenerated some options! Here are your new options:')
            print(self.state['player'][local_player]['move_choices'])
            print('')  # Print a newline to separate this regeneration section

    def send_state_to_opponent(self, connection_socket: socket):
        """
        Sends the current state as a string through the given socket.
        Returns a copy of the message sent.
        :param connection_socket: socket object representing the connection
        """
        # Encode state in outgoing message
        outgoing_message = self.encode_state()

        # Send the response message to update other player
        send_message(outgoing_message, connection_socket)

    def handle_new_message(self, incoming_message: str, connection_socket: socket) -> EndGameCode:
        """
        Plays one round of the game for either player, given an existing state.
        :param incoming_message: message received from the other host
        :param connection_socket: socket object representing the connection
        :return: end-game code defined in EndGameCode
        """
        # Check if stage is selected already.
        # Player 2 needs to update when player 1 selects a stage.
        changing_stage = True if self.state['stage'] is self._INITIAL_STAGE else False

        # Decode state in incoming message
        new_state = self.decode_state(incoming_message)

        # Replace local state with incoming state, no questions asked
        self.state = new_state

        # State is received after opponent updated it for their turn. Change it back to local player's turn
        self.change_turn()

        # Check if opponent quit
        if self.get_opponent_move() == QUIT_MESSAGE:
            return EndGameCode.OPPONENT_QUITS

        # Notify player 2 of the stage choice
        if changing_stage is True:
            self.print_stage_info()

        # (only player 1) calculate result and display it
        if self.state['whose_turn'] == PLAYER_1:
            self.handle_end_of_round()

        # Get local player's next move
        self.play_next_move()

        # Update opponent
        self.send_state_to_opponent(connection_socket)

        # Check if local player quit
        if self.get_local_player_move() == QUIT_MESSAGE:
            return EndGameCode.LOCAL_PLAYER_QUITS

        # (only player 2) calculate result and display it
        if self.state['whose_turn'] == PLAYER_2:
            self.handle_end_of_round()

        return EndGameCode.CONTINUE

    def play_game(self, connection_socket: socket):
        """
        Interacts with another host until sending or receiving a quit message.
        Starts interaction by receiving.
        :param connection_socket: socket object representing the connection
        """
        # Initialize the first message's data with the first packet's data
        try:
            packet_data = receive_next_packet(connection_socket)

        except PacketUnpackError:
            print(PACKET_RECEIVE_ERROR_MESSAGE)
            return

        is_last_packet = packet_data['is_last_packet']
        packet_payload = packet_data['payload']
        incoming_message_payload = packet_payload

        # Receive and reply to messages in packets from client until a message matches the quit message
        while incoming_message_payload != QUIT_MESSAGE:
            # If this packet is the first of a new message, process the message that just finished transmitting.
            # The request message payload is now completely received.
            if is_last_packet is True:
                # Process the complete message
                endgame_code = self.handle_new_message(incoming_message_payload, connection_socket)

                # Check for end of game by local player
                if endgame_code == EndGameCode.LOCAL_PLAYER_QUITS:
                    self.handle_endgame()

                    return

                elif endgame_code == EndGameCode.OPPONENT_QUITS:
                    self.handle_endgame()
                    print('\nOpponent quit. You are the RPS master today.')

                    return

                # Reset to track the new message
                incoming_message_payload = ''

                # Tell local player to wait for opponent
                print(WAITING_FOR_OPPONENT_MESSAGE)

            # Receive a packet of data from the other host
            try:
                packet_data = receive_next_packet(connection_socket)

            except PacketUnpackError:
                print(PACKET_RECEIVE_ERROR_MESSAGE)
                return

            is_last_packet = packet_data['is_last_packet']
            packet_payload = packet_data['payload']

            # Add this packet's payload to the message text
            incoming_message_payload += packet_payload
