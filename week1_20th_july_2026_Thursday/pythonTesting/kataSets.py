
# Kata Set-1
from dataclasses import dataclass
class InsufficientFundsError(Exception):
    def __init__(self, message, balance, amount):
        super().__init__(message)
        self.balance = balance
        self.amount = amount

    def __str__(self):
        return (
            f"{self.args[0]}\n"
            f"Current Balance: {self.balance}\n"
            f"Requested Amount: {self.amount}"
        )

@dataclass
class BankAccount:
    name: str
    accId: int
    Balance: int
    
    
    def withdraw(self,amount):
        if amount > self.Balance:
            raise InsufficientFundsError("Insufficient Funds",self.Balance, amount)
        
        self.Balance -= amount  
    
a = BankAccount('Subhan',1507,167)
b = BankAccount('Subhan',1507,167)

try:
    print(a==b)
    a.withdraw(160)
except InsufficientFundsError as e:
    print(e)
    
print(a)

# Kata Set-2
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

# Kata Set-3

class InsufficientFundsError(Exception):
    def __init__(self,message,balance,amount):
        super().__init__(message)
        self.message = message
        self.balance = balance
        self.amount = amount
    
    def __str__(self):
        return f"{self.message}.\nYour Current Balance: {self.balance}.\nYour Entered Amount: {self.amount}.\nPlease Enter Relevant Amount  "

class bankAccount:
    
    def __init__(self,name,accId,Balance=0):
        self.name = name
        self.accId = accId
        self.Balance = Balance
        
    def withDraw(self, amount):
        if(amount > self.Balance):
            raise InsufficientFundsError("InSufficient Amount",self.Balance, amount)
        else:
            self.Balance -= amount
            
    def __str__(self):
        return f"Name: {self.name} \nAccount ID: {self.accId} \nBalance: {self.Balance}"
        
        
account = bankAccount('Subhan',1507,167)

try:
    account.withDraw(200)
except InsufficientFundsError as e:
    print(e)
    
print(account)

import pytest

def test_withdraw_success():
    account = bankAccount("Subhan",1507,300)
    account.withDraw(200)
    assert account.Balance == 100
    
def test_withdraw_insufficient_error():
    account = bankAccount("Subhan",1507,300)
    with pytest.raises(InsufficientFundsError):
        account.withDraw(1000)
        
        
# Kata Set-4
@pytest.fixture
def account():
    return bankAccount("Subhan",1507,500)

def test_withdraw_success(account):
    account.withDraw(200)
    assert account.Balance == 300
    
def test_withdraw_insufficient_balance(account):
    with pytest.raises(InsufficientFundsError):
        account.withDraw(1000)