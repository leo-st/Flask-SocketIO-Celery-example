from functools import wraps
from time import process_time
def measure(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(process_time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(process_time() * 1000)) - start
            print(
                f"Total execution time {func.__name__}: {end_ if end_ > 0 else 0} ms (or {(end_/60000 if end_ > 0 else 0):.2f} min or {(end_/3600000 if end_ > 0 else 0):.2f} h)"
            )

    return _time_it
