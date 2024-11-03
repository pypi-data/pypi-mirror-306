import pytest
from src.packaging_demo.app import add, mul

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(-1, -1) == -2

def test_mul():
    assert mul(2, 3) == 6
    assert mul(-1, 1) == -1
    assert mul(0, 5) == 0
    assert mul(-2, -3) == 6

if __name__ == "__main__":
    pytest.main()