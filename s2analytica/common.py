# import time

from datetime import datetime

from s2analytica.settings import AUTHENTICATED_RATE_LIMIT, IST, UNAUTHENTICATED_RATE_LIMIT

def log_time(func):
    # This function shows the execution time of 
    # the function object passed
    def wrap_func(*args, **kwargs):
        

        t1 = datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S.%f')
        # print starting time in ist
        print(f'Started at {t1}')
        result = func(*args, **kwargs)
        t2 = datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S.%f')

        # print ending time in ist
        print(f'Ended at {t2}')
        # print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func



getratelimit = lambda _, request: AUTHENTICATED_RATE_LIMIT if request.user.is_authenticated else UNAUTHENTICATED_RATE_LIMIT

