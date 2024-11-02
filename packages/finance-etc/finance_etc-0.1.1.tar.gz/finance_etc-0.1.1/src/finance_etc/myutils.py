from functools import wraps
def print_deco(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        print(ret)
        return ret
    return wrapper