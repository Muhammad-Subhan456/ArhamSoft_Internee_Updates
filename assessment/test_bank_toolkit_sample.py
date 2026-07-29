from datetime import datetime

import pytest

from bank_toolkit.bank_toolkit import (
    Bank,
    BankAccount,
    InsufficientFundsError,
    SavingsAccount,
    is_business_hours,
)


def test_deposit_happy():
    a = BankAccount("Alice", 100.0)
    a.deposit(50.0)
    assert a.balance == 150.0


def test_withdraw_insufficient_funds_raises():
    a = BankAccount("Alice", 50.0)
    with pytest.raises(InsufficientFundsError):
        a.withdraw(100.0)


def test_savingsaccount_apply_interest():
    s = SavingsAccount("Alice", 100.0, interest_rate=0.1)
    s.apply_interest()
    assert s.balance == pytest.approx(110.0)


def test_bank_total_assets():
    bank = Bank()
    bank.add_account(BankAccount("Alice", 100.0))
    bank.add_account(BankAccount("Bob", 50.0))
    assert bank.total_assets() == 150.0


def test_is_business_hours_weekday_daytime():
    assert is_business_hours(datetime(2026, 7, 22, 10, 0)) is True