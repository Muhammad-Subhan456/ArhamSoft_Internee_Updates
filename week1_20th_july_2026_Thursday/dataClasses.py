from dataclasses import dataclass

# init: Add .__init__() method? (Default is True.)
# repr: Add .__repr__() method? (Default is True.)
# eq: Add .__eq__() method? (Default is True.)
# order: Add ordering methods? (Default is False.)
# unsafe_hash: Force the addition of a .__hash__() method? (Default is False.)
# frozen: If True, assigning to fields raise an exception. (Default is False.)


@dataclass
class Information:
    name: str
    age: int = 0.0  #Works same as init function initialization
    
    
print(Information('Subhan',23))


from dataclasses import dataclass, field
@dataclass
class Student:
    name: str
    tags: list = field(default_factory=list)
    
s1 = Student("Subhan")
s2 = Student("Tayyab") 

s1.tags.append("Python")
print(s1.tags)
print(s2.tags)