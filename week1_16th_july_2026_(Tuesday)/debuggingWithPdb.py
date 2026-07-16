# import os


# def get_path(filename):
#     """Return file's path or empty string if no path."""
#     head, tail = os.path.split(filename)
#     import pdb; pdb.set_trace()
#     return head


# filename = __file__
# print(f'path = {get_path(filename)}')

def multiply(a, b):
    return a * b

def calculate():
    x = 5
    y = 10

    breakpoint()

    result = multiply(x, y)

    print(result)

calculate()