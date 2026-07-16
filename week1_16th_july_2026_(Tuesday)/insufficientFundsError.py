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