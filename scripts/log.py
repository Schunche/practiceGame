import time

class Color:
    """
    Utility class for applying ANSI color codes to text.
    """

    color_codes: dict[str, str] = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m"
    }

    @classmethod
    def apply(cls, text: str, color_name: str) -> str:
        """
        Apply color to the given text.

        Args:
            text (str): The text to colorize.
            color_name (str): The name of the color to apply.

        Returns:
            str: The colorized text.
        """
        color_code = cls.color_codes.get(color_name, "")
        return f"{color_code}{text}{cls.color_codes['reset']}"

def logMSG(msg) -> None:
    """
    Log a message with a timestamp in white color.

    Args:
        msg (str): The message to log.
    """
    print(Color.apply(f"{time.asctime()} :> {msg}", "white"))

def logError(msg) -> None:
    """
    Log an error message with a timestamp in red color.

    Args:
        msg (str): The error message to log.
    """
    print(Color.apply(f"{time.asctime()} :> ERROR - {msg}", "red"))
