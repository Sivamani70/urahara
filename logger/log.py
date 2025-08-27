class CustomLogger:
    """
    A custom logger class to print colored and formatted messages to the console.
    It uses ANSI escape codes to add color and boldness to different log levels.
    """

    # ANSI escape codes as class attributes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"

    def error(self, message: str):
        """
        Prints a bold red error message.

        Args:
            message (str): The error message to be printed.
        """
        print(f"{self.BOLD}{self.RED}[ERROR]::{message}{self.RESET}")

    def info(self, message: str):
        """
        Prints a yellow info message.

        Args:
            message (str): The informational message to be printed.
        """
        print(f"{self.YELLOW}[INFO]::{message}{self.RESET}")

    def success(self, message: str):
        """
        Prints a bold green success message.

        Args:
            message (str): The success message to be printed.
        """
        print(f"{self.BOLD}{self.GREEN}[SUCCESS]::{message}{self.RESET}")
