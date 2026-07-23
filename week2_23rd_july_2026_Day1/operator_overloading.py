
# Object creation: __new__, __init__
# Object representation: __repr__, __str__
# Comparisons & operators: __eq__, __add__, etc.
# Attribute access: __getattribute__, __getattr__, __setattr__
# Iteration: __iter__, __next__
# Callable objects: __call__
# Context managers: __enter__, __exit__
# Collection behavior: __len__, __getitem__, __setitem__, __delitem__, __contains__


class BankAccount:

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def __add__(self, other):
        return self.balance + other.balance
    
a = BankAccount("A",10)
b = BankAccount("B",20)
print(a+b)


# The in Operator:
class ShopingCart:
    def __init__(self):
        self.items = ["A","B","C"]
        
    def __contains__(self, item):
        return item in self.items
    
cart = ShopingCart()
print("A" in cart)


# Augmented Assignment
class BankAccount:

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def __iadd__(self, amount):
        self.balance += amount
        return self
    
account = BankAccount("Ali", 1000)

account += 500

print(account.balance)