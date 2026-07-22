"""A small expense tracker."""

from dataclasses import dataclass, field
from functools import lru_cache, wraps
import json


@dataclass
class Expense:
    amount: float
    category: str
    tags: list = field(default_factory=list)


class NegativeAmountError(Exception):
    """Raised when an expense amount is negative."""
    pass


def add_expense(amount, category, expenses=None):
    if expenses is None:
        expenses = []
    if amount < 0:
        raise NegativeAmountError(f"amount cannot be negative: {amount}")
    expenses.append(Expense(amount, category, []))
    return expenses


def load_expenses_from_file(path):
    try:
        with open(path) as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return []
    


def iter_expenses(expenses):
    for e in expenses:
        yield e


def total_of(expenses_gen):
    return sum(e.amount for e in expenses_gen)


def summarize_by_category(expenses):
    return {
        c: [e.amount for e in expenses if e.category == c and e.amount > 0 and len(e.tags) >= 0]
        for c in {e.category for e in expenses}
    }


# @lru_cache
def category_multiplier(category, rates):
    # print(category)
    # print(rates)
    return rates.get(category, 1.0)


def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


@log_call
def apply_discount(expense, pct):
    expense.amount = expense.amount * (1 - pct)
    return expense


def build_category_reporters(expenses):
    """Return one report-generating function per category."""
    categories = sorted({e.category for e in expenses})
    reporters = []
    for cat in categories:
        reporters.append(lambda cat=cat : f"{cat}: {sum(e.amount for e in expenses if e.category == cat)}")
    return reporters


if __name__ == "__main__":

    print("Expense tracker demo starting...")
    demo_expenses = add_expense(42.50, "food")
    demo_expenses = add_expense(15.00, "transport", demo_expenses)
    print ("Demo Expenses: ",demo_expenses)

    rates = {"food": 1.1, "transport": 1.0}
    print(f"Food multiplier: {category_multiplier('food', rates)}")

    discounted = apply_discount(demo_expenses[0], 0.1)
    print(f"Discount fn reports its own name as: {apply_discount.__name__}")

    expenses_gen = iter_expenses(demo_expenses)
    print(f"Demo total: {total_of(expenses_gen)}")
    print(f"Demo total again: {total_of(expenses_gen)}")

    print("Per-category reports:")
    for report in build_category_reporters(demo_expenses):
        print(f"  {report()}")
        
    file_data = load_expenses_from_file("data.json")
    print(type(file_data))
    print(file_data)