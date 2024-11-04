import pytest
from funky_fortune.main import lucky_number

def test_lucky_number():
    assert 0 <= lucky_number("RandomName") < 100

def test_lucky_number_consistency():
    assert lucky_number("sameName") == lucky_number("sameName")

def test_lucky_number_edge_cases():
    assert lucky_number("") == 0
    assert 0 <= lucky_number("123!@#") < 100

def test_lucky_number_range():
    test_cases = [
        "A" * 1000,  # Very long name
        "Hello World!",  # With spaces and punctuation
        "12345",  # Only numbers
        "测试",  # Unicode characters
        "    ",  # Only spaces
    ]
    for test_case in test_cases:
        result = lucky_number(test_case)
        assert isinstance(result, int)
        assert 0 <= result < 100

def test_lucky_number_special_chars():
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    result = lucky_number(special_chars)
    assert isinstance(result, int)
    assert 0 <= result < 100