from .color import Color

def print_with_color(*values: object, color: Color) -> None:
    """
    Prints the given values in a specified color.

    :param values: The values to print.
    :param color: The color to use for the text, specified by a Color Enum.
    """
    print(f"{color.value}{' '.join(map(str, values))}{Color.RESET.value}")


def print_error(*values: object) -> None:
    """
    Prints the given values in red to indicate an error message.

    :param values: The values to print, which represent an error message.
    """
    print_with_color(*values, color=Color.RED)


def print_title(*values: object) -> None:
    """
    Prints the given values in green to indicate a title or header.

    :param values: The values to print, representing the title or header text.
    """
    print_with_color(*values, color=Color.GREEN)


def print_rainbow(*values: object) -> None:
    """
    Prints the provided values in a rainbow color pattern.

    :param values: The values to be printed, each character colored sequentially in rainbow colors.
    """
    rainbow_colors = [Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE, Color.PURPLE]
    text = " ".join(map(str, values))

    colored_text = "".join(
        f"{rainbow_colors[i % len(rainbow_colors)].value}{char}"
        for i, char in enumerate(text)
    )
    print(colored_text + Color.RESET.value)
