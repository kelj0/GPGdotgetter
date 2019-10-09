import random
import string


def generateRandomString(N):
    '''Returns random string of N chars long'''
    return ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits
            ) for _ in range(N)
        )
