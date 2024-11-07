import random


def generate_password(length=6):
    """
    Generates a random password.

    Args:
        length (int, optional): Length of the generated password. Defaults to 6.

    Returns:
        str: Generated password (e.g. Wv4Bs3Dv2Wz5Eq1Xe2).
    """
    MAYUS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    MINUS = list('abcdefghijklmnopqrstuvwxyz')
    NUMBERS = list('0123456789')
    # SPECIAL = list('!@#$%^&*()_+-=[]{}|;:,.<>/?')

    PASSWORD = ''
    for i in range(length):
        PASSWORD += random.choice(MAYUS)
        PASSWORD += random.choice(MINUS)
        PASSWORD += random.choice(NUMBERS)
        # PASSWORD += random.choice(SPECIAL)

    return PASSWORD
