
# For a traceback, always follow this order:
# 1) Last line → What exception occurred?
# 2) Frame immediately above it → Where was it raised?
# 3) Remaining frames above → How did the program get there?

class InsufficientFundsError(Exception):
    pass


class BankAccount:
    def __init__(self, owner, account_no, balance):
        self.owner = owner
        self.account_no = account_no
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient balance")
        self.balance -= amount


def make_transaction():
    account = BankAccount("Faraz", 1507, 500)
    account.withdraw(1000)


make_transaction()