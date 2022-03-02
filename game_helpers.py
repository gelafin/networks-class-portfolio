# Author: Mark Mendez
# Date: 03/01/2022

import json
from socket_helpers import *
from game_constants import *


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
            'whose_turn': '1',  # 1 or 2 (player 1 or player 2)
            'stage': self._INITIAL_STAGE,  # one of the constant STAGE options
            'player': {
                '1': _INITIAL_PLAYER_STATE,
                '2': _INITIAL_PLAYER_STATE
            }
        }

    def handle_endgame(self):
        """
        Shows final score
        """
        print('final scores: placeholder')

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
        self.set_player_move_options('1', initial_move_options)
        self.set_player_move_options('2', initial_move_options)

    def set_player_move(self, player: str, move: str):
        """
        Sets the move of the given player in game state
        :param player: 1 or 2 (player 1 or player 2)
        :param move: R, P, or S
        """
        self.state['player'][player]['current_move'] = move

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

    def play_next_move(self) -> str:
        """
        Shows players' remaining move options and prompts current player for a new move.
        Sets current player's move selection.
        """
        # Show both players' remaining move options
        local_player_move_options = self.get_player_move_options('1')
        print(f'Your remaining options:{local_player_move_options}')

        # Your turn--what's your move?
        move_selection = input('your next move (R / P / S): ')

        # Record the move selection
        self.set_player_move(self.state['whose_turn'], move_selection)

        return move_selection

    def get_local_player_move(self) -> str:
        """
        Returns the most recent move chosen by the local player
        :return: local player's most recent move; R, P, or S
        """
        local_player = None

        if self.state['whose_turn'] == '1':
            local_player = '1'
        elif self.state['whose_turn'] == '2':
            local_player = '2'
        local_player_move = self.state['player'][local_player]['current_move']

        return local_player_move

    def get_opponent_move(self) -> str:
        """
        Returns the most recent move chosen by the opponent of the local player
        :return: opponent's most recent move; R, P, or S
        """
        opponent = None

        if self.state['whose_turn'] == '2':
            opponent = '1'
        elif self.state['whose_turn'] == '1':
            opponent = '2'

        opponent_move = self.state['player'][opponent]['current_move']

        return opponent_move

    def change_turn(self):
        """
        Changes who the current player is.
        In this game, both players take their turn at the same time,
        but they are processed one at a time.
        This method helps keep track of which player is being processed.
        """
        if self.state['whose_turn'] == '2':
            self.state['whose_turn'] = '1'
        elif self.state['whose_turn'] == '1':
            self.state['whose_turn'] = '2'

    def handle_end_of_round(self):
        """
        Calculates and displays result of one round, after both players have taken their turn
        """
        # Award point based on who won, or no point if a tie

        # Display results
        # Show opponent's move choice
        print(f'{REPLY_LINE_PREFIX}{self.get_opponent_move()}')
        print('You both win this round, because this is a placeholder')
        print('Current score: placeholder')

        # Regenerate move choices if remaining move options have dwindled too much,
        # so the game can continue until a player quits
        print('(after some rounds) You randomly regenerated a placeholder!')

    def send_state_to_opponent(self, connection_socket: socket) -> str:
        """
        Sends the current state as a string through the given socket.
        Returns a copy of the message sent.
        :param connection_socket: socket object representing the connection
        :return: a copy of the new outgoing message
        """
        # Encode state in outgoing message
        outgoing_message = self.encode_state()

        # Send the response message to update other player
        send_message(outgoing_message, connection_socket)

        return outgoing_message

    def handle_new_message(self, incoming_message: str, connection_socket: socket) -> str:
        """

        :param incoming_message: message received from the other host
        :param connection_socket: socket object representing the connection
        :return: a copy of the new outgoing message
        """
        # Check if stage is selected already.
        # Player 2 needs to update when player 1 selects a stage.
        changing_stage = True if self.state['stage'] is self._INITIAL_STAGE else False

        # Decode state in incoming message
        new_state = self.decode_state(incoming_message)

        # Replace local state with incoming state, no questions asked
        # print('DEBUG: local state is currently...')
        # print(json.dumps(self.state, indent=1))
        self.state = new_state
        # print('DEBUG: received NEW state from opponent and set local state to...')
        # print(json.dumps(self.state, indent=1))

        # State is received after opponent updated it for their turn. Change it back to local player's turn
        self.change_turn()

        # Check if opponent quit
        if self.get_opponent_move() == QUIT_MESSAGE:
            return QUIT_MESSAGE

        # Notify player 2 of the stage choice
        if changing_stage is True:
            self.print_stage_info()

        # (only player 1) calculate result and display it
        if self.state['whose_turn'] == '1':
            self.handle_end_of_round()

        # Get local player's next move
        self.play_next_move()

        # Update opponent
        outgoing_message = self.send_state_to_opponent(connection_socket)

        # Check if local player quit
        if self.get_local_player_move() == QUIT_MESSAGE:
            return QUIT_MESSAGE

        # (only player 2) calculate result and display it
        if self.state['whose_turn'] == '2':
            self.handle_end_of_round()

        return outgoing_message

    def play_game(self, connection_socket: socket):
        """
        Interacts with another host until sending or receiving a quit message.
        Starts interaction by receiving.
        :param connection_socket: socket object representing the connection
        """
        # Initialize the first message's data with the first packet's data
        packet_data = receive_next_packet(connection_socket)
        is_last_packet = packet_data['is_last_packet']
        packet_payload = packet_data['payload']
        incoming_message_payload = packet_payload

        # Receive and reply to messages in packets from client until a message matches the quit message
        while incoming_message_payload != QUIT_MESSAGE:
            # If this packet is the first of a new message, process the message that just finished transmitting.
            # The request message payload is now completely received.
            if is_last_packet is True:
                # Process the complete message
                outgoing_message = self.handle_new_message(incoming_message_payload, connection_socket)

                # Check for end of game by local player
                if outgoing_message == QUIT_MESSAGE:
                    self.handle_endgame()
                    return

                # Reset to track the new message
                incoming_message_payload = ''

            # Receive a packet of data from the other host
            packet_data = receive_next_packet(connection_socket)
            is_last_packet = packet_data['is_last_packet']
            packet_payload = packet_data['payload']

            # Add this packet's payload to the message text
            incoming_message_payload += packet_payload

        # Display partner's quit message, to notify user of intentional connection close
        print(f'{REPLY_LINE_PREFIX}{incoming_message_payload}')
