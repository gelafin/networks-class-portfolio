# Author: Mark Mendez
# Date: 03/01/2022

QUIT_MESSAGE = '\\q'
QUIT_MESSAGE_PRINTABLE = r'\q'

# Message printed when local process encounters an error receiving a packet from the opponent process
PACKET_RECEIVE_ERROR_MESSAGE = 'Opponent had an error.'

# Use strings to represent players, so they can be used in dicts
# and are compatible with the json library
PLAYER_1 = '1'
PLAYER_2 = '2'

# Represent a tie.
# This should have the same data type as the players but represent neither of them.
TIE = 'tie'

# Choose a string that will distinguish replies
REPLY_LINE_PREFIX = 'vs '

# Define which moves are defeated by a given move
MOVE_PRIORITY = {
    'R': 'S',
    'P': 'R',
    'S': 'P'
}

# The game guarantees that both players always have at least this many move options
REGEN_THRESHOLD = 3

# Define stage choices
STAGES = {
    'HEAVEN': {
        'R': 3,
        'P': 3,
        'S': 3,
    },
    'OFFICE': {
        'R': 1,
        'P': 2,
        'S': 2,
    },
    'RAINFOREST': {
        'R': 2,
        'P': 3,
        'S': 1,
    },
    'MOUNTAIN': {
        'R': 2,
        'P': 1,
        'S': 1,
    },
    'ASTEROID': {
        'R': 3,
        'P': 1,
        'S': 2,
    },
    'ARMORY': {
        'R': 2,
        'P': 1,
        'S': 3,
    },
}

# Choose the message that displays to the client player who selects the stage
STAGE_CHOICE_PROMPT = ('You are player 1.\n\nChoose a stage by entering its name. ' +
                       'R, P, and S show how many of Rock, Paper, and Scissors each player gets.\n\n' +
                       f'{STAGES}\n\n'
                       )
