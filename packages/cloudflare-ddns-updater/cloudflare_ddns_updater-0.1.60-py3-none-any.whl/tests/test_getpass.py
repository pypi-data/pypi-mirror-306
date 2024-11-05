import os
import sys
from getpass import getpass


def secure_input():
    prompt = "Enter your API token"
    try:
        # Check for compliant terminal and use `getpass`
        if os.isatty(sys.stdin.fileno()):
            # This only runs `getpass` if the terminal supports hidden input
            return getpass(f"{prompt} (hidden input): ")
        else:
            raise EnvironmentError("Non-compliant terminal for hidden input.")
    except (ImportError, EnvironmentError):
        # Handle fallback for non-compliant terminals
        return input(f"{prompt} (Warning: Input will be visible): ")

# Test the secure_input function
token = secure_input()
