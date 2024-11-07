import random


class PasswordGenerator:
    def __init__(self, length=6):
        self.length = length

    def generate_password(self):
        """
        Generates a random password.

        Returns:
            str: Generated password.
        """
        MAYUS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        MINUS = list('abcdefghijklmnopqrstuvwxyz')
        NUMBERS = list('0123456789')
        # SPECIAL = list('!@#$%^&*()_+-=[]{}|;:,.<>/?')

        ALL_CHARACTERS = MAYUS + MINUS + NUMBERS
        PASSWORD = ''.join(random.choice(ALL_CHARACTERS)
                           for _ in range(self.length))

        return PASSWORD
