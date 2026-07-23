
# Kata Set-1
class NegativeAmountError(Exception):
    pass

class InsufficientFundsError(Exception):
    def __init__(self,message,balance,amount):
        super().__init__(message)
        self.message = message
        self.balance = balance
        self.amount = amount
    
    def __str__(self):
        return f"{self.message}.\nYour Current Balance: {self.balance}.\nYour Entered Amount: {self.amount}.\nPlease Enter Relevant Amount  "


class BankAccount:
    def __init__(self,owner,balance):
        if balance < 0:
            raise NegativeAmountError("Initial Balance Cannot Be Negative")
        
        self.owner = owner
        self.balance = balance
        
    def deposit(self, amount):
        if amount < 0:
            raise NegativeAmountError("Deposited Balance Cannot be Negative")
        
        self.balance += amount
        
    def withdraw(self,amount):
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient Balance",self.balance, amount)
        
        self.balance -= amount
        
    def __repr__(self):
        return (
            f"Bank Account: (owner='{self.owner}'), Balance = {self.balance}"
        )
        
    def __eq__(self, value):
        return( self.owner == value.owner and self.balance == value.balance)
    
if __name__ == '__main__':
    
    try:
        a = BankAccount("Ali", 1000)
        b = BankAccount("Ali", 1000)
        c = BankAccount("Ahmed", 500)
        print(a)
        print(a==b)
        print(b==c)
    except NegativeAmountError as e:
        print(e)
    
    
# Kata Set-2
try:
    # Instance Style
    account1 = BankAccount("Subhan",1000)
    account1.deposit(500)
    # Class Style
    BankAccount.deposit(account1,500)
    account2 = BankAccount.__new__(BankAccount)
    BankAccount.__init__(account2,"Tayyab",300)
    BankAccount.deposit(account2,2001)
    print(account1)
    print(account2)
    print(vars(account1))
except NegativeAmountError as e:
    print(e)
except InsufficientFundsError as e:
    print(e)


# Kata Set-3
try:
    acc = BankAccount("Abdullah",1000)
    acc.withdraw(2000)
    print(acc)
except InsufficientFundsError as e:
    print(e)
    
# Kata Set-4
class bankaccount:
    def __init__(self,balance):
        self.__balance = balance
        
class SavingsAccount(bankaccount):
    def __init__(self, balance,savings_balance):
        super().__init__(balance)
        self.__balance = savings_balance
        
account = SavingsAccount(1000,5000)
print(vars(account))
print(account._bankaccount__balance)
print(account._SavingsAccount__balance)

# Kata Set-5
from dataclasses import dataclass
@dataclass
class BankAccount:
    owner: str
    balance: float
# Specific Line a data class could not generate:
    # if balance < 0:
    #     raise NegativeAmountError("Balance cannot be negative")
    # Solution:
    def __post_init__(self): # Custom initialization logic in a data class
        if self.balance < 0:
            raise NegativeAmountError("Balance cant be negative")
        

try:        
    account = BankAccount("Faraz",-1)
    print(account)
except NegativeAmountError as e:
    print(e)