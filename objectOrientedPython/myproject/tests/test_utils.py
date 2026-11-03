# test_utils.py
from myproject.utils import greet

def test_greet():
    assert greet("Redd") == "Hello, Redd"
