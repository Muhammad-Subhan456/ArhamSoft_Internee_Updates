
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
            f"{type(self).__name__}: (owner='{self.owner}'), Balance = {self.balance}"
        )
        
    def __eq__(self, value):
        return( self.owner == value.owner and self.balance == value.balance)
    
    # Kata Set-4
    def summary(self):
        return(
            f"================================\n"
            f"Account Type: {type(self).__name__}\n"
            f"Owner Name: {self.owner}\n"
            f"Account Balance: {self.balance}\n"
            f"================================\n"
            
        )
    
# Kata Set-2

class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance) # Calls Parent Constructor
        self.interest_rate = interest_rate
    
    # Kata Set-3    
    def __repr__(self):
        parent = super().__repr__()
        return (
            f"{parent}, "
            f"interest_rate= {self.interest_rate}"
        )
        
    def summary(self):
        return(

            f"================================\n"
            f"Account Type: {type(self).__name__}\n"
            f"Owner Name: {self.owner}\n"
            f"Account Balance: {self.balance}\n"
            f"Interest Rate: {self.interest_rate}\n"            
            f"================================\n"

        )
        
def print_all(accounts):
    for acc in accounts:
        print(acc.summary())
        
# Kata Set-5
# Bank should not inherit from BankAccount because a bank is not a type of account,it has many 
# accounts, making composition i.e "has a" relationship instead of inheritance (is a) relationship 
class Bank:
    def __init__(self):
        self.accounts = []
    
    def add_account(self,account):
        self.accounts.append(account)
    
    def total_assets(self):
        total = 0
        for acc in self.accounts:
            total += acc.balance
        
        return total
        

if __name__ == '__main__':
            
    bank_account = BankAccount("Subhan",300)
    savings_account = SavingsAccount("Tayyab",400,10)
    print(bank_account)
    print(savings_account)
    
    accounts = [

    BankAccount("Tayyab",1000),

    SavingsAccount("Subhan",5000,8),

    BankAccount("Faraz",700)]
    print_all(accounts)
    
    bank = Bank()
    bank.add_account(bank_account)
    bank.add_account(savings_account)
    
    print("Bank Total Asset: ", bank.total_assets())
