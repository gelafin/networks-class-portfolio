# Author: Mark Mendez
# Date: 03/01/2022

QUIT_MESSAGE = '\\q'

# Choose a string that will distinguish replies
REPLY_LINE_PREFIX = 'vs '

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
STAGE_CHOICE_PROMPT = ('You are player 1.\n\nChoose a stage by entering its name.' +
                       'R, P, and S show how many of Rock, Paper, and Scissors each player gets.\n' +
                       f'{STAGES}'
                       )