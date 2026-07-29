from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor

import asyncio
import json
import logging
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Callable

logger = logging.getLogger(__name__)


class InsufficientFundsError(Exception):
    """Raised when a withdrawal would exceed the account balance."""


class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        # Owner must be a non-empty string
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Owner Must Be A Non-Empty String")

        # Balance cannot be negative
        if balance < 0:
            raise ValueError("Balance Cannot Be Negative")    
        
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        # Reject zero and negative values
        if amount <= 0:
            raise ValueError("Deposited Amount Must Be Positive")
        
        self.balance += amount
        logger.info(
            "Deposited %.2f into %s's account. New Balance: %.2f",
            amount,
            self.owner,
            self.balance
        )

    def withdraw(self, amount: float) -> None:
        # Negative amount should never be with drawed
        if amount < 0:
            raise ValueError("WithDrawal amount must be positive")
        
        
        if amount > self.balance + 1e-9:
            logger.warning(
                "Account '%s' has insufficient funds for withdrawal.",
                self.owner,
            )
            raise InsufficientFundsError("InSufficient Funds")
        
        self.balance -= amount
        logger.info(
        "Withdrew %.2f from %s's account. New balance: %.2f",
        amount,
        self.owner,
        self.balance,
    )

    def __repr__(self) -> str:
        return f"{type(self).__name__}(owner='{self.owner}', balance={self.balance})"

    def __eq__(self, other: object) -> bool:
        
        if type(other) is not type(self):
            return False

        return (
            self.owner == other.owner
            and self.balance == other.balance
        )


class SavingsAccount(BankAccount):
    def __init__(self, owner: str, balance: float = 0.0, interest_rate: float = 0.0) -> None:
        # Calling the parent constructor
        super().__init__(owner,balance)

        if interest_rate < 0:
            raise ValueError("Interest Rate Cannot Be Negative")

        self.interest_rate = interest_rate

    def apply_interest(self) -> None:
        self.balance += self.balance * self.interest_rate

    def __repr__(self) -> str:
        #  Call Parent Class __repr__
        parent_repr = super().__repr__()
        return (
            f"{parent_repr[:-1]}, "
            f"interest_rate={self.interest_rate})"
        )

    def __eq__(self, other: object) -> bool:
        if not super().__eq__(other):
            return False
        return self.interest_rate == other.interest_rate 


class Bank:
    def __init__(self) -> None:
        self.accounts: list[BankAccount] = []

    def add_account(self, account: BankAccount) -> None:
        if not isinstance(account,BankAccount):
            raise TypeError(
                "account must be a BankAccount or SavingsAccount."
            )
        self.accounts.append(account)


    def total_assets(self) -> float:
        return sum(account.balance for account in self.accounts)

    def summary_by_owner(self) -> dict[str, float]:
        # Dictionary stores new owner's balance at 0.0
        summary = defaultdict(float)
        
        for account in self.accounts:
            summary[account.owner] += account.balance
        
        return dict(summary)


def save_accounts(path: Path, accounts: list[BankAccount]) -> None:
    
    # Convert account objects into JSON-serializable dictionaries.
    data = []

    for account in accounts:
        if isinstance(account, SavingsAccount):
            data.append(
                {
                    "type": "SavingsAccount",
                    "owner": account.owner,
                    "balance": account.balance,
                    "interest_rate": account.interest_rate,
                }
            )
        else:
            data.append(
                {
                    "type": "BankAccount",
                    "owner": account.owner,
                    "balance": account.balance,
                }
            )

    # Creating parent directories 
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write to Json file.
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    


def load_accounts(path: Path) -> list[BankAccount]:

    # Reading the JSON file.
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    accounts = []

    # Reconstructing each account object.
    for account_data in data:
        if account_data["type"] == "BankAccount":
            account = BankAccount(
                owner=account_data["owner"],
                balance=account_data["balance"],
            )

        elif account_data["type"] == "SavingsAccount":
            account = SavingsAccount(
                owner=account_data["owner"],
                balance=account_data["balance"],
                interest_rate=account_data["interest_rate"],
            )

        else:
            raise ValueError(
                f"Unknown account type: {account_data['type']}"
            )

        accounts.append(account)

    return accounts


def count_by_type(accounts: list[BankAccount]) -> Counter:
    return Counter(
        type(account).__name__
        for account in accounts
    )


def is_business_hours(dt: datetime) -> bool:
    return dt.weekday() < 5 and 9 <= dt.hour < 17


def apply_interest_to_all(accounts: list[SavingsAccount]) -> None:
    with ThreadPoolExecutor() as executor:
        list(executor.map(SavingsAccount.apply_interest, accounts))


def fetch_rates_concurrently(symbols: list[str], fetch_fn: Callable[[str], float]) -> dict[str, float]:
    rates = {}

    with ThreadPoolExecutor() as executor:
        future_to_symbol = {
            executor.submit(fetch_fn, symbol): symbol
            for symbol in symbols
        }

        for future, symbol in future_to_symbol.items():
            try:
                rates[symbol] = future.result()
            except Exception as error:
                logger.warning(
                    "Failed to fetch rate for %s: %s",
                    symbol,
                    error,
                )

    return rates


async def apply_interest_async(accounts: list[SavingsAccount]) -> None:
    async def apply(account: SavingsAccount) -> None:
        await asyncio.sleep(0.05)
        account.apply_interest()

    await asyncio.gather(
        *(apply(account) for account in accounts)
    )