import random
import string


def load_random_string(num, seed=None):
    randStr = ''
    if not seed:
        seed = string.ascii_letters + string.digits
    for _ in range(num):
        randStr += seed[random.randrange(1, len(seed))]
    return randStr


def get_basic_data(request):
    ret = {}
    if request.user.is_authenticated:
        ret['user'] = request.user
    return ret
