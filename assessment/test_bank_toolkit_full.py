from __future__ import annotations

import asyncio
import json
import math
from datetime import datetime
from pathlib import Path

import pytest

from bank_toolkit.bank_toolkit import (
    InsufficientFundsError,
    BankAccount,
    SavingsAccount,
    Bank,
    save_accounts,
    load_accounts,
    count_by_type,
    is_business_hours,
    apply_interest_to_all,
    fetch_rates_concurrently,
    apply_interest_async,
)


# ---------------------------------------------------------------------------
# BankAccount: construction
# ---------------------------------------------------------------------------

class TestBankAccountInit:
    def test_default_balance_is_zero(self):
        acc = BankAccount("Alice")
        assert acc.balance == 0.0
        assert acc.owner == "Alice"

    def test_positive_balance_accepted(self):
        acc = BankAccount("Alice", 100.0)
        assert acc.balance == 100.0

    def test_zero_balance_accepted(self):
        acc = BankAccount("Alice", 0.0)
        assert acc.balance == 0.0

    def test_negative_balance_raises(self):
        with pytest.raises(ValueError):
            BankAccount("Alice", -0.01)

    def test_large_negative_balance_raises(self):
        with pytest.raises(ValueError):
            BankAccount("Alice", -1_000_000)

    def test_owner_empty_string_allowed(self):
        # The implementation does not validate owner names; document current
        # (permissive) behavior so a future change is caught by this test.
        acc = BankAccount("", 10)
        assert acc.owner == ""

    def test_owner_none_allowed_by_implementation(self):
        # No type-checking exists on `owner`; this documents that reality.
        acc = BankAccount(None, 10)  # type: ignore[arg-type]
        assert acc.owner is None

    def test_float_precision_balance(self):
        acc = BankAccount("Alice", 0.1 + 0.2)
        assert math.isclose(acc.balance, 0.3, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# BankAccount: deposit
# ---------------------------------------------------------------------------

class TestBankAccountDeposit:
    def test_deposit_increases_balance(self):
        acc = BankAccount("Alice", 100)
        acc.deposit(50)
        assert acc.balance == 150

    def test_deposit_negative_raises(self):
        acc = BankAccount("Alice", 100)
        with pytest.raises(ValueError):
            acc.deposit(-1)

    def test_deposit_zero_is_allowed_by_current_implementation(self):
        # NOTE: the inline comment says "Reject zero and negative values"
        # but the guard is `amount < 0`, so 0 actually passes through.
        # This test pins down the *actual* runtime behavior so any future
        # fix to match the comment is a deliberate, visible change.
        acc = BankAccount("Alice", 100)
        acc.deposit(0)
        assert acc.balance == 100

    def test_multiple_deposits_accumulate(self):
        acc = BankAccount("Alice", 0)
        for amount in (10, 20, 30.5):
            acc.deposit(amount)
        assert acc.balance == pytest.approx(60.5)

    def test_deposit_very_large_amount(self):
        acc = BankAccount("Alice", 0)
        acc.deposit(1e18)
        assert acc.balance == 1e18

    def test_deposit_logs_info(self, caplog):
        acc = BankAccount("Alice", 0)
        with caplog.at_level("INFO"):
            acc.deposit(25)
        assert any("Deposited" in record.message for record in caplog.records)


# ---------------------------------------------------------------------------
# BankAccount: withdraw
# ---------------------------------------------------------------------------

class TestBankAccountWithdraw:
    def test_withdraw_decreases_balance(self):
        acc = BankAccount("Alice", 100)
        acc.withdraw(40)
        assert acc.balance == 60

    def test_withdraw_negative_raises(self):
        acc = BankAccount("Alice", 100)
        with pytest.raises(ValueError):
            acc.withdraw(-5)

    def test_withdraw_exact_balance_to_zero(self):
        acc = BankAccount("Alice", 100)
        acc.withdraw(100)
        assert acc.balance == 0

    def test_withdraw_more_than_balance_raises_insufficient_funds(self):
        acc = BankAccount("Alice", 50)
        with pytest.raises(InsufficientFundsError):
            acc.withdraw(50.01)

    def test_withdraw_zero_allowed_and_no_op(self):
        acc = BankAccount("Alice", 50)
        acc.withdraw(0)
        assert acc.balance == 50

    def test_withdraw_insufficient_funds_logs_warning(self, caplog):
        acc = BankAccount("Alice", 10)
        with caplog.at_level("WARNING"):
            with pytest.raises(InsufficientFundsError):
                acc.withdraw(20)
        assert any(
            "insufficient funds" in record.message.lower()
            for record in caplog.records
        )

    def test_withdraw_from_zero_balance_raises(self):
        acc = BankAccount("Alice", 0)
        with pytest.raises(InsufficientFundsError):
            acc.withdraw(0.01)

    def test_withdraw_floating_point_edge_raises_due_to_representation_error(self):
        # 0.1 + 0.2 == 0.30000000000000004 in binary floating point, which
        # is *greater* than the stored balance of 0.3. Because withdraw()
        # uses a strict `amount > self.balance` comparison (no epsilon
        # tolerance), this "should" be a valid full withdrawal but instead
        # raises InsufficientFundsError. This test documents that real
        # floating-point edge case in the current implementation.
        acc = BankAccount("Alice", 0.3)
        with pytest.raises(InsufficientFundsError):
            acc.withdraw(0.1 + 0.2)

    def test_withdraw_matching_float_representation_succeeds(self):
        # When the exact same floating-point literal is used for both the
        # balance and the withdrawal amount, the comparison is exact and
        # the withdrawal succeeds, reducing the balance to zero.
        acc = BankAccount("Alice", 0.1 + 0.2)
        acc.withdraw(0.1 + 0.2)
        assert acc.balance == 0


# ---------------------------------------------------------------------------
# BankAccount: repr / eq
# ---------------------------------------------------------------------------

class TestBankAccountDunder:
    def test_repr_format(self):
        acc = BankAccount("Alice", 100)
        assert repr(acc) == "BankAccount(owner='Alice', balance=100)"

    def test_eq_same_owner_and_balance(self):
        assert BankAccount("Alice", 100) == BankAccount("Alice", 100)

    def test_eq_different_balance(self):
        assert BankAccount("Alice", 100) != BankAccount("Alice", 200)

    def test_eq_different_owner(self):
        assert BankAccount("Alice", 100) != BankAccount("Bob", 100)

    def test_eq_against_non_account_returns_false(self):
        acc = BankAccount("Alice", 100)
        assert (acc == "Alice") is False
        assert (acc == 100) is False
        assert (acc == None) is False  # noqa: E711
        assert (acc == object()) is False

    def test_eq_is_reflexive(self):
        acc = BankAccount("Alice", 100)
        assert acc == acc

    def test_savings_account_equals_plain_account_same_fields(self):
        # __eq__ only checks isinstance(other, BankAccount) plus owner and
        # balance, so a SavingsAccount (a BankAccount subclass) that shares
        # owner/balance is considered equal to a plain BankAccount even
        # though interest_rate differs. This documents that (surprising)
        # current behavior explicitly.
        plain = BankAccount("Alice", 100)
        savings = SavingsAccount("Alice", 100, interest_rate=0.05)
        assert plain == savings
        assert savings == plain


# ---------------------------------------------------------------------------
# SavingsAccount
# ---------------------------------------------------------------------------

class TestSavingsAccount:
    def test_inherits_balance_validation(self):
        with pytest.raises(ValueError):
            SavingsAccount("Alice", -10, 0.05)

    def test_default_interest_rate_zero(self):
        acc = SavingsAccount("Alice", 100)
        assert acc.interest_rate == 0.0

    def test_apply_interest_increases_balance(self):
        acc = SavingsAccount("Alice", 100, interest_rate=0.1)
        acc.apply_interest()
        assert acc.balance == pytest.approx(110)

    def test_apply_interest_zero_rate_no_change(self):
        acc = SavingsAccount("Alice", 100, interest_rate=0.0)
        acc.apply_interest()
        assert acc.balance == 100

    def test_apply_interest_negative_rate_decreases_balance(self):
        # No validation exists on interest_rate, so negative rates are
        # accepted and shrink the balance.
        acc = SavingsAccount("Alice", 100, interest_rate=-0.5)
        acc.apply_interest()
        assert acc.balance == pytest.approx(50)

    def test_apply_interest_repeatedly_compounds(self):
        acc = SavingsAccount("Alice", 100, interest_rate=0.10)
        acc.apply_interest()
        acc.apply_interest()
        assert acc.balance == pytest.approx(121)

    def test_repr_includes_interest_rate_but_hardcodes_class_name(self):
        # BankAccount.__repr__ hardcodes the literal string "BankAccount"
        # instead of using type(self).__name__, so SavingsAccount.__repr__
        # (which reuses the parent repr via super()) prints "BankAccount(...)"
        # rather than "SavingsAccount(...)" even though `acc` really is a
        # SavingsAccount. This test pins down that real, currently-shipped
        # quirk so any future fix is a visible, intentional change.
        acc = SavingsAccount("Alice", 100, interest_rate=0.05)
        assert repr(acc) == (
            "BankAccount(owner='Alice', balance=100, interest_rate=0.05)"
        )
        assert type(acc).__name__ == "SavingsAccount"  # the object itself is correct

    def test_withdraw_and_deposit_inherited(self):
        acc = SavingsAccount("Alice", 100, interest_rate=0.05)
        acc.deposit(50)
        acc.withdraw(30)
        assert acc.balance == 120

    def test_isinstance_of_bank_account(self):
        acc = SavingsAccount("Alice", 100)
        assert isinstance(acc, BankAccount)


# ---------------------------------------------------------------------------
# Bank
# ---------------------------------------------------------------------------

class TestBank:
    def test_new_bank_has_no_accounts(self):
        bank = Bank()
        assert bank.accounts == []
        assert bank.total_assets() == 0

    def test_add_account_appends(self):
        bank = Bank()
        acc = BankAccount("Alice", 100)
        bank.add_account(acc)
        assert bank.accounts == [acc]

    def test_add_account_rejects_non_account_type(self):
        bank = Bank()
        with pytest.raises(TypeError):
            bank.add_account("not an account")  # type: ignore[arg-type]

    def test_add_account_rejects_none(self):
        bank = Bank()
        with pytest.raises(TypeError):
            bank.add_account(None)  # type: ignore[arg-type]

    def test_add_account_accepts_savings_subclass(self):
        bank = Bank()
        bank.add_account(SavingsAccount("Alice", 100, 0.02))
        assert len(bank.accounts) == 1

    def test_total_assets_sums_all_balances(self):
        bank = Bank()
        bank.add_account(BankAccount("Alice", 100))
        bank.add_account(SavingsAccount("Bob", 250, 0.03))
        assert bank.total_assets() == 350

    def test_total_assets_with_zero_accounts(self):
        assert Bank().total_assets() == 0

    def test_summary_by_owner_aggregates_same_owner(self):
        bank = Bank()
        bank.add_account(BankAccount("Alice", 100))
        bank.add_account(SavingsAccount("Alice", 50, 0.1))
        summary = bank.summary_by_owner()
        assert summary == {"Alice": 150}

    def test_summary_by_owner_multiple_owners(self):
        bank = Bank()
        bank.add_account(BankAccount("Alice", 100))
        bank.add_account(BankAccount("Bob", 200))
        summary = bank.summary_by_owner()
        assert summary == {"Alice": 100, "Bob": 200}

    def test_summary_by_owner_empty_bank_returns_empty_dict(self):
        assert Bank().summary_by_owner() == {}


# ---------------------------------------------------------------------------
# save_accounts / load_accounts
# ---------------------------------------------------------------------------

class TestPersistence:
    def test_round_trip_bank_account(self, tmp_path: Path):
        path = tmp_path / "accounts.json"
        original = [BankAccount("Alice", 100)]
        save_accounts(path, original)
        loaded = load_accounts(path)
        assert loaded == original
        assert isinstance(loaded[0], BankAccount)
        assert not isinstance(loaded[0], SavingsAccount)

    def test_round_trip_savings_account(self, tmp_path: Path):
        path = tmp_path / "accounts.json"
        original = [SavingsAccount("Bob", 200, 0.04)]
        save_accounts(path, original)
        loaded = load_accounts(path)
        assert isinstance(loaded[0], SavingsAccount)
        assert loaded[0].interest_rate == 0.04
        assert loaded[0] == original[0]

    def test_round_trip_mixed_accounts_preserves_order(self, tmp_path: Path):
        path = tmp_path / "accounts.json"
        original = [
            BankAccount("Alice", 100),
            SavingsAccount("Bob", 200, 0.05),
            BankAccount("Carol", 0),
        ]
        save_accounts(path, original)
        loaded = load_accounts(path)
        assert loaded == original
        assert [type(a).__name__ for a in loaded] == [
            "BankAccount",
            "SavingsAccount",
            "BankAccount",
        ]

    def test_save_creates_parent_directories(self, tmp_path: Path):
        nested = tmp_path / "a" / "b" / "c" / "accounts.json"
        save_accounts(nested, [BankAccount("Alice", 10)])
        assert nested.exists()

    def test_save_empty_list_writes_empty_json_array(self, tmp_path: Path):
        path = tmp_path / "empty.json"
        save_accounts(path, [])
        assert json.loads(path.read_text()) == []

    def test_save_overwrites_existing_file(self, tmp_path: Path):
        path = tmp_path / "accounts.json"
        save_accounts(path, [BankAccount("Alice", 1)])
        save_accounts(path, [BankAccount("Bob", 2)])
        loaded = load_accounts(path)
        assert loaded == [BankAccount("Bob", 2)]

    def test_load_unknown_account_type_raises(self, tmp_path: Path):
        path = tmp_path / "bad.json"
        path.write_text(json.dumps([{"type": "GhostAccount", "owner": "X", "balance": 1}]))
        with pytest.raises(ValueError):
            load_accounts(path)

    def test_load_missing_file_raises_file_not_found(self, tmp_path: Path):
        missing = tmp_path / "does_not_exist.json"
        with pytest.raises(FileNotFoundError):
            load_accounts(missing)

    def test_load_malformed_json_raises_json_decode_error(self, tmp_path: Path):
        path = tmp_path / "broken.json"
        path.write_text("{not: valid json,,,")
        with pytest.raises(json.JSONDecodeError):
            load_accounts(path)

    def test_load_missing_required_field_raises_key_error(self, tmp_path: Path):
        path = tmp_path / "incomplete.json"
        path.write_text(json.dumps([{"type": "BankAccount", "owner": "Alice"}]))
        with pytest.raises(KeyError):
            load_accounts(path)

    def test_saved_file_is_valid_json_with_indentation(self, tmp_path: Path):
        path = tmp_path / "accounts.json"
        save_accounts(path, [BankAccount("Alice", 10)])
        text = path.read_text()
        assert "\n" in text  # indent=4 implies newlines present
        json.loads(text)  # should not raise


# ---------------------------------------------------------------------------
# count_by_type
# ---------------------------------------------------------------------------

class TestCountByType:
    def test_empty_list(self):
        assert count_by_type([]) == {}

    def test_only_bank_accounts(self):
        accounts = [BankAccount("A", 1), BankAccount("B", 2)]
        result = count_by_type(accounts)
        assert result == {"BankAccount": 2}

    def test_mixed_types(self):
        accounts = [
            BankAccount("A", 1),
            SavingsAccount("B", 2, 0.1),
            SavingsAccount("C", 3, 0.1),
        ]
        result = count_by_type(accounts)
        assert result["BankAccount"] == 1
        assert result["SavingsAccount"] == 2

    def test_returns_counter_instance(self):
        from collections import Counter

        result = count_by_type([BankAccount("A", 1)])
        assert isinstance(result, Counter)


# ---------------------------------------------------------------------------
# is_business_hours
# ---------------------------------------------------------------------------

class TestIsBusinessHours:
    def test_monday_at_9am_is_business_hours(self):
        # 2024-01-01 is a Monday
        assert is_business_hours(datetime(2024, 1, 1, 9, 0)) is True

    def test_monday_at_4_59pm_is_business_hours(self):
        assert is_business_hours(datetime(2024, 1, 1, 16, 59)) is True

    def test_monday_at_5pm_is_not_business_hours(self):
        # Upper bound is exclusive (hour < 17)
        assert is_business_hours(datetime(2024, 1, 1, 17, 0)) is False

    def test_monday_at_8_59am_is_not_business_hours(self):
        # Lower bound is inclusive (hour >= 9); 8:59 should fail
        assert is_business_hours(datetime(2024, 1, 1, 8, 59)) is False

    def test_saturday_during_business_hours_is_false(self):
        # 2024-01-06 is a Saturday
        assert is_business_hours(datetime(2024, 1, 6, 10, 0)) is False

    def test_sunday_during_business_hours_is_false(self):
        # 2024-01-07 is a Sunday
        assert is_business_hours(datetime(2024, 1, 7, 10, 0)) is False

    def test_friday_is_last_valid_weekday(self):
        # 2024-01-05 is a Friday
        assert is_business_hours(datetime(2024, 1, 5, 12, 0)) is True

    def test_midnight_is_not_business_hours(self):
        assert is_business_hours(datetime(2024, 1, 1, 0, 0)) is False

    def test_exactly_midnight_next_day_boundary(self):
        assert is_business_hours(datetime(2024, 1, 1, 23, 59)) is False


# ---------------------------------------------------------------------------
# apply_interest_to_all (threaded)
# ---------------------------------------------------------------------------

class TestApplyInterestToAll:
    def test_applies_interest_to_every_account(self):
        accounts = [
            SavingsAccount("A", 100, 0.1),
            SavingsAccount("B", 200, 0.2),
        ]
        apply_interest_to_all(accounts)
        assert accounts[0].balance == pytest.approx(110)
        assert accounts[1].balance == pytest.approx(240)

    def test_empty_list_does_not_raise(self):
        apply_interest_to_all([])  # should simply do nothing

    def test_single_account(self):
        accounts = [SavingsAccount("A", 100, 0.5)]
        apply_interest_to_all(accounts)
        assert accounts[0].balance == pytest.approx(150)

    def test_many_accounts_all_updated(self):
        accounts = [SavingsAccount(f"user{i}", 100, 0.01) for i in range(50)]
        apply_interest_to_all(accounts)
        assert all(acc.balance == pytest.approx(101) for acc in accounts)


# ---------------------------------------------------------------------------
# fetch_rates_concurrently
# ---------------------------------------------------------------------------

class TestFetchRatesConcurrently:
    def test_all_symbols_succeed(self):
        rates = fetch_rates_concurrently(
            ["USD", "EUR"], lambda symbol: {"USD": 1.0, "EUR": 0.9}[symbol]
        )
        assert rates == {"USD": 1.0, "EUR": 0.9}

    def test_empty_symbol_list_returns_empty_dict(self):
        assert fetch_rates_concurrently([], lambda s: 1.0) == {}

    def test_failing_symbol_is_omitted_not_raised(self):
        def fetch_fn(symbol: str) -> float:
            if symbol == "BAD":
                raise RuntimeError("boom")
            return 1.0

        rates = fetch_rates_concurrently(["USD", "BAD", "EUR"], fetch_fn)
        assert "BAD" not in rates
        assert rates == {"USD": 1.0, "EUR": 1.0}

    def test_all_symbols_fail_returns_empty_dict(self):
        def fetch_fn(symbol: str) -> float:
            raise ValueError("nope")

        rates = fetch_rates_concurrently(["USD", "EUR"], fetch_fn)
        assert rates == {}

    def test_duplicate_symbols_only_last_result_kept(self):
        # future_to_symbol is keyed by future, so duplicate symbol strings
        # each get their own future/result, but the final `rates` dict can
        # only have one entry per (duplicate) key.
        calls = []

        def fetch_fn(symbol: str) -> float:
            calls.append(symbol)
            return float(len(calls))

        rates = fetch_rates_concurrently(["USD", "USD"], fetch_fn)
        assert "USD" in rates
        assert len(calls) == 2  # fetch_fn was invoked for each duplicate

    def test_logs_warning_on_failure(self, caplog):
        def fetch_fn(symbol: str) -> float:
            raise RuntimeError("network down")

        with caplog.at_level("WARNING"):
            fetch_rates_concurrently(["USD"], fetch_fn)
        assert any("Failed to fetch rate" in r.message for r in caplog.records)


# ---------------------------------------------------------------------------
# apply_interest_async
# ---------------------------------------------------------------------------

class TestApplyInterestAsync:
    def test_applies_interest_to_all_accounts(self):
        accounts = [
            SavingsAccount("A", 100, 0.1),
            SavingsAccount("B", 200, 0.5),
        ]
        asyncio.run(apply_interest_async(accounts))
        assert accounts[0].balance == pytest.approx(110)
        assert accounts[1].balance == pytest.approx(300)

    def test_empty_list_does_not_raise(self):
        asyncio.run(apply_interest_async([]))

    def test_single_account_zero_rate(self):
        accounts = [SavingsAccount("A", 100, 0.0)]
        asyncio.run(apply_interest_async(accounts))
        assert accounts[0].balance == 100

    def test_runs_concurrently_not_sequentially(self):
        # With N accounts each "sleeping" 0.05s concurrently, the whole
        # gather should take roughly 0.05s, not N * 0.05s. This guards
        # against someone accidentally serializing the awaits.
        import time

        accounts = [SavingsAccount(f"user{i}", 100, 0.01) for i in range(20)]
        start = time.perf_counter()
        asyncio.run(apply_interest_async(accounts))
        elapsed = time.perf_counter() - start
        assert elapsed < 0.05 * 20  # generously below fully-sequential time
        assert all(acc.balance == pytest.approx(101) for acc in accounts)


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-v"]))