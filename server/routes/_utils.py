import os


def check_key(key):
    return key == os.getenv('API_KEY')
