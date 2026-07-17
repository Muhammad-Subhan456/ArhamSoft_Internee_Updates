from functools import lru_cache
import time

# with cache Finished in 0.0007 sec
# # without cache Finished in 34.1088 sec
# @lru_cache → "Remember previous results so the function doesn't recompute them."
# partial() → "Create a new function with some arguments already filled in."

# @lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Finished in {end - start:.4f} secs")
        return result
    return wrapper


@timer
def run():
    return fib(40)

print(run())