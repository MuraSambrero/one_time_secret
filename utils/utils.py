import os
import datetime


def generate_crypt_string() -> str:
    number_of_symbols = 10
    crypt_rand_string = os.urandom(number_of_symbols).hex()
    return crypt_rand_string


def time_to_end(seconds: int = 7*24*3600) -> datetime:
    return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
