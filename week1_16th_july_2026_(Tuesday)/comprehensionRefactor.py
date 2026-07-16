
# Conventional way
squares = []
for x in range(10):
    squares.append(x**2)
    
print(squares)

# Using List Comprehensions
squares = list(map(lambda x : x**2, range(10) ))
print(squares)

# other method of comprehension
squares = [x**2 for x in range(10)]
print(squares)

# List comp with 2 lists
list1 = [1,2,3]
list2 = [3,1,4]

result = [(x,y) for x in list1 for y in list2 if x != y]
print(result)

# Tuple comprehensions
names = ['   Subhan  ', '   Tayyab', 'Ali   '  ]
result = [name.strip() for name in names]
print(result)

# List of 2 Tuples:
result = [(x,x**2) for x in range(10) ]
print(result)

# Flattening a 2D List
vec = [[1,2,3], [4,5,6], [7,8,9]]
result = [num for row in vec for num in row]
print(result)

#Dictionaries
info = {'Subhan':22, 'Ali': 19}
print(info.get('Tayyab'))

# using dictionary constructor
information = dict([('Subhan',22),('Ali',23) ])
print(information)

# Dict Comprehensions
example = { x : x*2 for x in (2,4,6) }
print(example)

# Looping through Dictionaries
for k,v in information.items():
    print(k,v)
    
    
#Practice
# Part-1: Refactor a verbose Loop into a list comprehension
numbers = [1,2,3,4,5,6,7,8,9]
# Task: Keep only the Even Numbers
# Verbose Loop:
even = []
for num in numbers:
    if num % 2 == 0:
        even.append(num)
        
print(even)
# Refactored with List Comprehension (Filter)
even = [num for num in numbers if num%2 == 0]
print(even)
# Task: Transform array elements to their cubes
# Verbose Loop:
cubes = []
for num in numbers:
    cubes.append(num**3)
    
print(cubes)
# List Comprehension Transformation
cubes = [num**3 for num in numbers ]
print(cubes)

# Part-2:
# Task: Refactor a verbose Loop into a dict comprehension
#Verbose Loop
names = ['Ali', 'Sara', 'Ahmad']
marks = [90,39,67]
result = {}

for name,mark in zip(names,marks):
    result[name] = mark
    
print(result)

# Dict Comprehension
result = {name: mark for name,mark in zip(names,marks)}
print(result)

#Comprehension which makes code worse
numbers = [1, 2, -3, 4, 100, 5, 6]
result = []
for num in numbers:
    if num < 0:
        continue
    elif num == 100:
        break
    else: 
        result.append(num**2)

print(result)

# Explanation: We didnt use Comprehension here because we avoid comprehensions when
# the expressions include break, continue, multiple independent stops and nested conditions
# as the above tasks include break and continue statement we used simple plain loop