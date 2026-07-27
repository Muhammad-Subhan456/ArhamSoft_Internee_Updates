import unittest

from models import BankAccount, NegativeAmountError


class TestBankAccount(unittest.TestCase):

    def test_deposit(self):
        account = BankAccount("Ali", 100)

        account.deposit(50)

        self.assertEqual(account.balance, 150)

    def test_negative_deposit(self):
        account = BankAccount("Ali", 100)

        with self.assertRaises(NegativeAmountError):
            account.deposit(-10)


if __name__ == "__main__":
    unittest.main()