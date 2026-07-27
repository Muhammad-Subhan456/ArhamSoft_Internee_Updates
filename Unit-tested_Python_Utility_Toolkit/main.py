from datetime import datetime
from collections import Counter, defaultdict
import logging
from pathlib import Path

from models import (
    BankAccount,
    InsufficientFundsError,
    save_transactions,
    load_transactions,
    transactions_today,
)

BASE_DIR = Path(__file__).resolve().parent

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "bank.log"),
        logging.StreamHandler(),
    ],
)

def main():

    account = BankAccount("Ali", 1000)

    account.deposit(300)
    account.withdraw(500)

    try:
        account.withdraw(5000)

    except InsufficientFundsError as e:
        logging.error(e)


    transactions = [
        {
            "owner": "Ali",
            "amount": 500,
            "date": datetime.now(),
        },
        {
            "owner": "Sara",
            "amount": 200,
            "date": datetime.now(),
        },
    ]

    transactions_file = BASE_DIR / "data" / "transactions.json"

    save_transactions(transactions_file, transactions)

    loaded = load_transactions(transactions_file)

    print(loaded)

    

    print(
        transactions_today(
            loaded
        )
    )

    

    transactions = [
        {
            "category": "Food",
            "amount": 25,
        },
        {
            "category": "Transport",
            "amount": 10,
        },
        {
            "category": "Food",
            "amount": 40,
        },
        {
            "category": "Shopping",
            "amount": 80,
        },
        {
            "category": "Food",
            "amount": 15,
        },
        {
            "category": "Transport",
            "amount": 20,
        },
    ]

    category_counts = Counter(
        transaction["category"]
        for transaction in transactions
    )

    print(category_counts)

    

    amounts_by_category = defaultdict(list)

    for transaction in transactions:

        amounts_by_category[
            transaction["category"]
        ].append(
            transaction["amount"]
        )

    print(dict(amounts_by_category))

    

    current_time = datetime.now()

    formatted_time = current_time.strftime(
        "%Y-%m-%d %I:%M:%S %p"
    )

    print(formatted_time)


if __name__ == "__main__":
    main()