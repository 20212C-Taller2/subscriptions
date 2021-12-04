import random
import string


def create_wallet():
    # TODO Integrate with wallet
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
