def string_input_parser(prompt: str):
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
            break
        except ValueError:
            print("something went wrong")
        except KeyboardInterrupt:
            print(
                "You pressed control-c, you want to quit? \n\n To quit press 'Q' \n To continue press 'C'"
            )
            cho = string_input_parser("Enter your choice: ")
            if cho == "Q" or cho == "q":
                exit()
            if cho == "C" or cho == "c":
                continue

    return parsed_value


def number_input_parser(prompt: str):
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
            print(
                "You pressed control-c ,you want to quit ? \n\n you want to quit press 'Q' you \n you want continue press 'C'"
            )
            choice = string_input_parser("enter your next step: ")
            if choice == "Q" or choice == "q":
                exit()
            if choice == "C" or choice == "c":
                continue

    return parsed_value
