from package.expense_tracker import add_expense
from package.expense_tracker import *
import pytest


@pytest.fixture
def expense_list():
    return [Expense(10,"food",[])]

# Already Present Test
def test_add_expense(expense_list):
    result = add_expense(10, "food")
    assert result == expense_list
    
# Negative Amount Test    
def test_negative_amount(expense_list):
    with pytest.raises(NegativeAmountError):
        add_expense(-10,"food",[])
    
# Test of My Choice 
def test_data_from_json(expense_list):
    result =  load_expenses_from_file("data.json")
    expense = add_expense(result["amount"],result["category"],[])
    assert expense == expense_list