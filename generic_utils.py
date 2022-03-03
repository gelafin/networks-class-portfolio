# Author: Mark Mendez
# Date: 03/02/2022
from typing import List


def print_iterable_items_directly(iterable):
    """
    Prints each item in an iterable, one at a time.
    This avoids using repr(), which is good for printing special characters.
    Source: https://stackoverflow.com/q/54471443/14257952
    :param iterable: any iterable collection
    """
    # Print each item
    for item in iterable:
        print(item, end=', ')

    # Print the usual newline, to mimic built-in behavior
    print('')


def get_validated_input(
        prompt: str, valid_options: List[str], error_message: str, show_valid_options_on_error: bool = False) -> str:
    """
    Wrapper for input() that adds whitelist validation
    :param prompt: message to display to user initially and when re-prompting after each error_message
    :param valid_options: options which would be valid input
    :param show_valid_options_on_error: if True, prints valid_options when input is invalid
    :param error_message: message to display when user enters invalid input
    :return: validated user input
    """
    # Get initial input
    current_input = input(prompt)

    # Reattempt input until getting something in valid_options
    while current_input not in valid_options:
        # Re-prompt
        print(error_message)

        if show_valid_options_on_error is True:
            print('You have to choose one of these options (no typos, case-sensitive):')
            print_iterable_items_directly(valid_options)

        current_input = input(prompt)

    return current_input
