
# # Kata Set-1
# from dataclasses import dataclass
# class InsufficientFundsError(Exception):
#     def __init__(self, message, balance, amount):
#         super().__init__(message)
#         self.balance = balance
#         self.amount = amount

#     def __str__(self):
#         return (
#             f"{self.args[0]}\n"
#             f"Current Balance: {self.balance}\n"
#             f"Requested Amount: {self.amount}"
#         )

# @dataclass
# class BankAccount:
#     name: str
#     accId: int
#     Balance: int
    
#     def withdraw(self,amount):
#         if amount > self.Balance:
#             raise InsufficientFundsError("Insufficient Funds",self.Balance, amount)
        
#         self.Balance -= amount  
    
# a = BankAccount('Subhan',1507,167)
# b = BankAccount('Subhan',1507,167)

# try:
#     print(a==b)
#     a.withdraw(160)
# except InsufficientFundsError as e:
#     print(e)
    
# print(a)

# # Kata Set-2
# from dataclasses import dataclass, field
# @dataclass
# class Student:
#     name: str
#     tags: list = field(default_factory=list)
    
# s1 = Student("Subhan")
# s2 = Student("Tayyab")

# s1.tags.append("Python")
# print(s1.tags)
# print(s2.tags)


# Kata Set-3
from week1_16th_july_2026_Tuesday.insufficientFundsError import InsufficientFundsError,bankAccount
import pytest

def test_withdraw_success():
    account = bankAccount("Subhan",1507,300)
    account.withDraw(200)
    assert account.Balance == 100
    
def test_withdraw_insufficient_error():
    account = bankAccount("Subhan",1507,300)
    with pytest.raises(InsufficientFundsError):
        account.withDraw(1000)