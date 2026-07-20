# Enumerate
# More readable
# No need to write ranges
# Give both index and element directly

names = ['a','b','c','d']
marks = [1,2,3,4]

for i , item in enumerate(names):
    print(i, item,end=' ')
    
print()
# zip iterate over multiple iterators
# zip ends when the shortest iterable ends
for name, mark in zip(names,marks):
    print(name,mark, end=' ')
    
# itertools.chain() - Treat Multiple iterables as One
# Benefit: Dont creates a new combined List
# More Memory Efficient, especially for large iterables

from itertools import chain
list1 = [1,2,3,4]
list2 = [2,3,4,5,6,7]
print()
for num in chain(list1,list2):
    print(num, end = ' ' )  


# Generators cant be sliced like list
# to slice the generators use itertools
# Benefit of using islice
# 1) Works directly with generators
# 2) Doesnt builds the entire sequence in memory
# 3) preserves laxzy evaluation

from itertools import islice
print()
gen = (x for x in range(10))
for num in islice(gen,2,5):
    print(num, end= ' ')