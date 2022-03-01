# Author: Mark Mendez
# Date: 02/23/2022

"""Define all constants used by http socket programs"""
QUIT_MESSAGE = '\\q'
PORT_NUMBER = 8011
# Note from recv() docs:
# For best match with hardware and network realities,
# the value of bufsize should be a relatively small power of 2, for example, 4096
BUFFER_SIZE = 1024

# Configure server details necessary for connection.
# This simple example only works with localhost.
SERVER_NAME = 'localhost'  # server hostname or IP address
SERVER_PORT = PORT_NUMBER  # arbitrary port > 1023 (source: previous assignment instructions) matching client

# In GELA372, the first byte of every packet is a "last packet" flag,
# and a receiver accumulates packets until detecting a flag of 1.
GELA372_LAST_PACKET_FALSE = '0'
GELA372_LAST_PACKET_TRUE = '1'

# Choose a string that will distinguish replies
REPLY_LINE_PREFIX = 'vs '

# Define stage choices
STAGES = {
    'OFFICE': [
        {'R': 1},
        {'P': 2},
        {'S': 2},
    ],
    'RAINFOREST': [
        {'R': 2},
        {'P': 3},
        {'S': 1},
    ],
    'MOUNTAIN': [
        {'R': 2},
        {'P': 1},
        {'S': 1},
    ],
    'ASTEROID': [
        {'R': 3},
        {'P': 1},
        {'S': 2},
    ],
    'ARMORY': [
        {'R': 2},
        {'P': 1},
        {'S': 3},
    ]
}

# Choose the message that displays to the client player who selects the stage
STAGE_CHOICE_PROMPT = ('You are player 1.\n\nChoose a stage by entering its name.' +
                       'R, P, and S show how many of Rock, Paper, and Scissors each player gets.\n' +
                       f'{STAGES}'
                       )
