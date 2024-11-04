import random
import string


def generateString():
    return "frankli_" + "".join(random.sample(string.ascii_lowercase, 7))
