# 
# Decorators: Allows to modify the behaviour of funcion without changing their actual Code.
# When you use a Python decorator, you wrap a function with another function, which takes the
# original function as an argument and returns its modified version
# Practical use cases for decorators include logging, enforcing access control, caching results,
# and measuring execution time.

def my_decorator(func):
    def wrapper():
        print("Before the function")
        func()
        print("After the function")
    return wrapper

@my_decorator
def greet():
    print("HELLO!")
    
greet()

# Real world Example: Use for logging
# Instead of printing everywhere we can use our decorator on every function

# Decorators with arguements
def log(func):
    def wrapper(*args,**kwargs):
        print("Function Started")
        result = func(*args,**kwargs)
        print("Function Ended")
        return result
    return wrapper

@log
def add(a,b):
    return a+b

print(add(3,5))

# `functools.wraps`

# When a function is decorated, the original function is replaced by the decorator's **wrapper** function.
# As a result, the decorated function loses its original metadata.

# Without `@functools.wraps(func)`:

# * `function.__name__` becomes `"wrapper"` instead of the original function name.
# * `function.__doc__` (docstring) is lost.
# * Other metadata (module, annotations, etc.) is replaced by the wrapper's metadata.
# * Debuggers, IDEs, documentation tools, and frameworks may display incorrect information.

# Using `@functools.wraps(func)` copies the original function's metadata to the wrapper, 
# so the decorated function still appears as the original function during introspection and debugging.

# Example:
from functools import wraps

def my_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result

    return wrapper

#Rule: Whenever you write a custom decorator with a `wrapper` function,
# use `@functools.wraps(func)` unless you have a specific reason not to.
