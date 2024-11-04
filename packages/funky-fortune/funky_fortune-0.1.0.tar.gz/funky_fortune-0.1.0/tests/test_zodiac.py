import pytest
from funky_fortune.main import zodiac_fortune

def test_zodiac_fortune():
    assert zodiac_fortune("Aries") in ["You'll meet a talking sheep today", "Watch out for ram horns", "Your wool sweater will bring good luck"]
    assert zodiac_fortune("Taurus") in ["Today is perfect for beef noodles", "You'll find a gold coin", "Don't be as stubborn as a bull"]

def test_zodiac_fortune_special_sign():
    assert zodiac_fortune("UnknownZodiac") == "Your zodiac sign is too special, I can't predict it"

def test_zodiac_fortune_case_sensitivity():
    assert zodiac_fortune("ARIES") == "Your zodiac sign is too special, I can't predict it"
    assert zodiac_fortune("aries") == "Your zodiac sign is too special, I can't predict it"

def test_zodiac_fortune_all_signs():
    all_signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    for sign in all_signs:
        fortune = zodiac_fortune(sign)
        assert isinstance(fortune, str)
        assert len(fortune) > 0

def test_zodiac_fortune_invalid_inputs():
    invalid_inputs = ["", " ", "123", None, "NotASign"]
    for invalid_input in invalid_inputs:
        assert zodiac_fortune(invalid_input) == "Your zodiac sign is too special, I can't predict it"