# Iterable
numbers = [10,20,30]

print(type(numbers))

for num in numbers:
    print(num)
    

# Iterator
it = iter(numbers)
print(type(it))
print(next(it))
print(next(it))
print(next(it))
print(next(it))