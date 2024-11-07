from secrets import choice
from string import digits, ascii_letters, ascii_lowercase, ascii_uppercase

keys = digits + ascii_uppercase + ascii_lowercase + ascii_letters

def generate_password(size: int = 8) -> str:
    """
    Create random password with given size
    :param size: size of password
    :return: random password
    """
    password = ""
    for i in range(size):
        password += ''.join(choice(keys))
    return password
