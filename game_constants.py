# Author: Mark Mendez
# Date: 03/01/2022

QUIT_MESSAGE = '\\q'

# Use strings to represent players, so they can be used in dicts
# and are compatible with the json library
PLAYER_1 = '1'
PLAYER_2 = '2'

# Choose a string that will distinguish replies
REPLY_LINE_PREFIX = 'vs '

# Define which moves are defeated by a given move
MOVE_PRIORITY = {
    'R': 'S',
    'P': 'R',
    'S': 'P'
}

# Define stage choices
STAGES = {
    'HEAVEN': [
        {'R': 3},
        {'P': 3},
        {'S': 3},
    ],
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
STAGE_CHOICE_PROMPT = ('You are player 1.\n\nChoose a stage by entering its name. ' +
                       'R, P, and S show how many of Rock, Paper, and Scissors each player gets.\n\n' +
                       f'{STAGES}\n\n'
                       )
