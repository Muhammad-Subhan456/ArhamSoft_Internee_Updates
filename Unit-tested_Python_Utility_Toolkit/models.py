from datetime import datetime
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)


class NegativeAmountError(Exception):
    pass


class InsufficientFundsError(Exception):
    def __init__(self, message, balance, amount):
        super().__init__(message)
        self.message = message
        self.balance = balance
        self.amount = amount

    def __str__(self):
        return (
            f"{self.message}.\n"
            f"Your Current Balance: {self.balance}.\n"
            f"Your Entered Amount: {self.amount}.\n"
            f"Please Enter Relevant Amount."
        )


class BankAccount:
    def __init__(self, owner: str, balance: float) -> None:
        if balance < 0:
            raise NegativeAmountError(
                "Initial Balance Cannot Be Negative"
            )

        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount < 0:
            raise NegativeAmountError(
                "Deposited Balance Cannot be Negative"
            )

        self.balance += amount

        logger.info(
            f"${amount} deposited into {self.owner}'s account."
        )

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:

            logger.warning(
                f"Failed withdrawal for {self.owner}. "
                f"Requested=${amount}, Available=${self.balance}"
            )

            raise InsufficientFundsError(
                "Insufficient Balance",
                self.balance,
                amount
            )

        self.balance -= amount

        logger.info(
            f"${amount} withdrawn from {self.owner}'s account."
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}: "
            f"(owner='{self.owner}'), "
            f"Balance={self.balance}"
        )

    def __eq__(self, value) -> bool:
        return (
            self.owner == value.owner
            and self.balance == value.balance
        )

    def summary(self) -> str:
        return (
            f"================================\n"
            f"Account Type: {type(self).__name__}\n"
            f"Owner Name: {self.owner}\n"
            f"Account Balance: {self.balance}\n"
            f"================================\n"
        )


class SavingsAccount(BankAccount):
    def __init__(
        self,
        owner: str,
        balance: float,
        interest_rate: int
    ) -> None:

        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def __repr__(self) -> str:
        parent = super().__repr__()

        return (
            f"{parent}, "
            f"interest_rate={self.interest_rate}"
        )

    def summary(self) -> str:
        return (
            f"================================\n"
            f"Account Type: {type(self).__name__}\n"
            f"Owner Name: {self.owner}\n"
            f"Account Balance: {self.balance}\n"
            f"Interest Rate: {self.interest_rate}\n"
            f"================================\n"
        )


def print_all(accounts: list[BankAccount]) -> None:
    for account in accounts:
        print(account.summary())


class Bank:
    def __init__(self) -> None:
        self.accounts: list[BankAccount] = []

    def add_account(
        self,
        account: BankAccount
    ) -> None:
        self.accounts.append(account)

    def total_assets(self) -> float:
        return sum(
            account.balance
            for account in self.accounts
        )


def save_transactions(
    path: str,
    transactions: list[dict]
) -> None:

    file_path = Path(path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    serializable = []

    for transaction in transactions:
        copy = transaction.copy()

        if "date" in copy:
            copy["date"] = copy["date"].isoformat()

        serializable.append(copy)

    file_path.write_text(
        json.dumps(serializable, indent=4),
        encoding="utf-8"
    )


def load_transactions(path: str) -> list[dict]:

    file_path = Path(path)

    if not file_path.exists():
        return []

    transactions = json.loads(
        file_path.read_text(
            encoding="utf-8"
        )
    )

    for transaction in transactions:

        if "date" in transaction:
            transaction["date"] = datetime.fromisoformat(
                transaction["date"]
            )

    return transactions


def transactions_today(
    transactions: list[dict]
) -> list[dict]:

    today = datetime.now().date()

    return [
        transaction
        for transaction in transactions
        if transaction["date"].date() == today
    ]