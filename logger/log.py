class CustomLogger:
    # ANSI escape codes as class attributes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"

    def error(self, message: str):
        """Prints a bold red error message."""
        print(f"{self.BOLD}{self.RED}[ERROR]::{message}{self.RESET}")

    def info(self, message: str):
        """Prints a yellow info message."""
        print(f"{self.YELLOW}[INFO]::{message}{self.RESET}")

    def success(self, message: str):
        """Prints a green success message."""
        print(f"{self.BOLD}{self.GREEN}[SUCCESS]::{message}{self.RESET}")
