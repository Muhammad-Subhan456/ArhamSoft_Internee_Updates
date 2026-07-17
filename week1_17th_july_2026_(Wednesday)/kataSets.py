# Kata set 1

def count_up_to(n):
    for i in range(1,n+1):
        yield i
        
for num in count_up_to(5):
    print(num, end = ' ')
    
    
# Kata Set 2
# Problem Here: Python computes every square immediately
# All results are storred in memory
# we cannot use any result until the loop is finished

numbers = [1, 2, 3, 4, 5]

squares = []

for num in numbers:
    squares.append(num ** 2)

print('\n',squares)

# Generator Function
# Benefit: Only one square computed when needed
# does not build a list in memory.
# generator pauses after each yield and resumes from that point when the next value is requested

def squareGenerator(nums):
    for num in nums:
        yield num**2    
        
for square in squareGenerator(numbers):
    print(square, end = ' ')
    
    
# Kata 3
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args,**kwargs):
        start_time = time.perf_counter()
        value = func(*args,**kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__}() in {run_time:.4f} secs")
        return value
    return wrapper_timer


# @timer
# def waste_some_time(num_times):
#     for _ in range(num_times):
#         sum([number**2 for number in range(10_000)])
        
# waste_some_time(1)
# waste_some_time(999)

# Kata 4

import json

@timer
def load_config(file_name):
    config = None

    try:
        with open(file_name, "r") as f:
            config = json.load(f)

    except FileNotFoundError:
        print("Config file not found")

    except json.JSONDecodeError:
        print("Config file is corrupted")

    finally:
        print(config)
        print("File closed")

    return config


# Call the function
config = load_config("config.json")


# Kata 5
# Exercise 1
fruits = ["Apple", "Banana", "Orange", "Mango"]

for i in range(len(fruits)):
    print(f"Index: {i}, Fruit: {fruits[i]}")
    
# Solution with iterTools
for i, fruit in enumerate(fruits):
    print(i, fruit, end=' ')
    
    
# Exercise 2    
names = ["Ali", "Sara", "Ahmad", "Ayesha"]
marks = [90, 85, 78, 92]

for i in range(len(names)):
    print(f"{names[i]} scored {marks[i]}")

# Solution with itertools
for name,mark in zip(names,marks):
    print(name,'=',mark, end=', ')
    
    
# Kata 6
from functools import lru_cache
import time

# with cache Finished in 0.0007 sec
# # without cache Finished in 34.1088 sec
# @lru_cache → "Remember previous results so the function doesn't recompute them."
# partial() → "Create a new function with some arguments already filled in."

@lru_cache(maxsize=None)
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