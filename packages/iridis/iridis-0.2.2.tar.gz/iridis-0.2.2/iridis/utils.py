from .color_prints import print_error


def get_number_from_user(
    input_text: str = "Vložte číslo: ",
    error_message: str = "Špatný vstup, zkuste znova!",
    conditions: list = None,
) -> float:
    """
    Prompts the user for a number input and validates it against optional conditions.

    :param input_text: The prompt text to display when asking for input (default is in Czech: "Vložte číslo").
    :param error_message: The error message to display in red in case of invalid input (default is in Czech: "Špatný vstup, zkuste znova!").
    :param conditions: A list of boolean conditions to validate the number against. If any condition fails, the error message is shown.
    :return: The valid number entered by the user.
    """
    while True:
        try:
            number = float(input(input_text))

            if conditions and not all(condition(number) for condition in conditions):
                print_error(error_message)
                continue

            return number
        except ValueError:
            print_error(error_message)
