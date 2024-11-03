import string
import secrets


def generate(size: int = 12, include_punctuation=False):
    pool = string.ascii_letters + string.digits
    if include_punctuation:
        pool += string.punctuation
    secret = "".join([secrets.choice(pool) for _ in range(size)])
    return secret
