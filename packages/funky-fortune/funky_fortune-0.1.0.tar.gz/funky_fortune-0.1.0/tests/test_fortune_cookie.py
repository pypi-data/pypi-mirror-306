import pytest
from funky_fortune.main import fortune_cookie

def test_fortune_cookie():
    assert fortune_cookie() in ["You'll be very lucky today", "Slow and steady wins the race", "Today is perfect for trying new things", "Remember to call your family"]
    assert fortune_cookie(lucky=True).startswith("Extra lucky: ")
    for _ in range(100):
        assert fortune_cookie().startswith("Extra lucky: ") == False

def test_fortune_cookie_lucky_consistency():
    for _ in range(50):
        fortune = fortune_cookie(lucky=True)
        assert fortune.startswith("Extra lucky: ")
        assert len(fortune) > 12  # "Extra lucky: " is 12 chars

def test_fortune_cookie_distribution():
    all_fortunes = set()
    for _ in range(100):
        all_fortunes.add(fortune_cookie())
    assert len(all_fortunes) >= 4  # Should have at least 4 different fortunes