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
        INITIAL_PLAYER_STATE = {
            'score': 0,
            'move_choices': None,
            'current_move': ''  # one of the R/P/S options
        }

        self.state = {
            'turn': 1,  # 1 or 2 (player 1 or player 2)
            'stage': '',  # one of the constant STAGE options
            'player': {
                '1': INITIAL_PLAYER_STATE,
                '2': INITIAL_PLAYER_STATE
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
        self.state['player'][player] = updated_options

    def set_stage(self, stage: str):
        """
        Updates player 2 to use the stage selected by player 1,
        and notifies player 2 of stage conditions.
        :param stage: message received from player 1
        """
        initial_move_options = STAGES[stage]

        print(f'Playing on stage {stage}')
        print(f'On {stage}, you both start with the following move options:')
        print(initial_move_options)

        self.state['stage'] = stage

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

    def prompt_next_move(self) -> str:
        """
        Shows players' remaining move options and prompts current player for a new move.
        Sets current player's move selection.
        """
        # Show both players' remaining move options
        local_player_move_options = self.get_player_move_options('1')
        print(f'Your remaining options:{local_player_move_options}')

        # Your turn--what's your move?
        outgoing_message = input('your next move (R / P / S): ')

        return outgoing_message

    def handle_new_message(self, incoming_message: str, connection_socket: socket) -> str:
        """
        Displays the received message, prompts for a reply message,
        and sends the reply message through the given socket.
        :param incoming_message: message received from the other host
        :param connection_socket: socket object representing the connection
        :return: a copy of the new outgoing message
        """
        # Decode state in incoming message
        new_state = self.decode_state(incoming_message)

        # Replace local state with incoming state, no questions asked
        self.state = new_state

        # Show the previous turn's result (if after the first move)
        # TODO: track local player's previous choice

        # Update score
        # TODO: track score

        # Get local player's next move
        self.prompt_next_move()

        # Show opponent's move choice
        print(f'{REPLY_LINE_PREFIX}{incoming_message}')

        # Regenerate move choices if remaining move options have dwindled too much,
        # so the game can continue until a player quits
        print('(after some rounds) You randomly regenerated a placeholder!')

        # Encode state in outgoing message
        outgoing_message = self.encode_state()

        # Send the response message to update other player
        send_message(outgoing_message, connection_socket)

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
                # Check for quit message
                if incoming_message_payload == QUIT_MESSAGE:
                    self.handle_endgame()
                    return

                # Check for stage selection message from player 1
                elif incoming_message_payload in STAGES:
                    self.set_stage(incoming_message_payload)

                # Process a normal message
                else:
                    outgoing_message = self.handle_new_message(incoming_message_payload, connection_socket)

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
