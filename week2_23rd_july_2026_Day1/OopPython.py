class Student:
    def __init__(self):
        self.name = "Ali"

s = Student()
print(s.__dict__)




class Student:

    @classmethod
    def create(cls):
        return cls()
    
print(Student())