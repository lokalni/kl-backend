import string
import shortuuid

DEFAULT_TOKEN_LENGTH = 6
DEFAULT_TOKEN_ALPHABET = '123456789' + string.ascii_uppercase[:36].replace('O', '')


def get_token(alphabet=DEFAULT_TOKEN_ALPHABET, length=DEFAULT_TOKEN_LENGTH):
    """Returns short human readable token."""
    return shortuuid.ShortUUID(alphabet=alphabet).random(length=length).upper()
