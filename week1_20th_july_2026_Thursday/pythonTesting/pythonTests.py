# PS> python -m venv venv
# PS> .\venv\Scripts\activate
# (venv) PS> python -m pip install pytest

def test_uppercase():
    assert "loud noise".upper().split() == "LOUD NOISE".split()
    
def test_reversed():
    assert list(reversed([1, 2, 3, 4])) == [4, 3, 2, 1]
    
import pytest

# Fixtures: Can create data, test doubles, initialize system state for the test suite

@pytest.fixture
def example_fixture():
    return 1

def test_with_fixture(example_fixture):
    assert example_fixture == 1