import sys
from typing import Any, Optional, Callable


def handle_keyboard_interrupt():
    """Exits the program or continues as usual"""
    print("You pressed control-c, you want to quit? \n\n To quit press 'Q' \n To continue press 'C'")
    choice = string_input_parser("enter your choice: ")
    if choice.casefold() == "Q".casefold():
        exit()
    if choice.casefold() == "C".casefold():
        return


def string_input_parser(prompt: str, validator: Optional[Callable[[str], bool]] = None) -> str:
    """
    Validates that a users input, provided to pythons `input()` function, is a string
    :param
        prompt: The prompt provided by a users input
    :returns:
        parsed_value: The parsed response provided by a user from the `input()` function
    """
    while True:
        try:
            parsed_value: str = input(prompt)
            if validator:
                is_valid = validator(parsed_value)
                if is_valid:
                    break
                continue
            break
        except ValueError as e:
            print(f"something went wrong with message: {e}")
        except KeyboardInterrupt:
            handle_keyboard_interrupt()
    return parsed_value


def integer_input_parser(prompt: str) -> Optional[int]:
    """
    Validates that a users input, provided to pythons `input()` function, is an integer
    The logic follows the following logic
    1. Tries to cast the input value to string
    2. Catches an invalid input and prompts the user again
    3. Catches `KeyboardInterrupt` and provides options to
        3.a. Quit the application
        3.b. Continue
    :param
        prompt: The prompt provided by a users input
    :returns:
        parsed_value: The parsed response provided by a user from the `input()` function
    """
    while True:
        try:
            parsed_value: int = int(input(prompt))
            break
        except ValueError:
            print("Please enter number not a word!")
        except KeyboardInterrupt:
            handle_keyboard_interrupt()
    return parsed_value


def is_valid_choice(input_value: Any, options: list) -> bool:
    # TODO: Depreciate in favour of a better structure; maybe fold into the parsers?
    return input_value in options
