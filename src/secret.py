from os.path import exists
import secrets
import sys


class Secret():
    def __init__(self):
        self.__app_secret = self.__get_secret()

    def get_secret(self):
        return self.__app_secret

    def __get_secret(self):
        is_file_exists = exists('secret')
        if not is_file_exists:
            secret = secrets.token_hex()
            file = open('secret', 'w')
            file.write(secret)
            file.close()
        else:
            file = open('secret', 'r')
            secret = file.read()
        return secret


sys.modules[__name__] = Secret()
