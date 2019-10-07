import random
import string


class StringHandler:

    @staticmethod
    def get_random_string(length=8):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
