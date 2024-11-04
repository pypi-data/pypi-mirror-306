import pytest
from funky_fortune.main import zodiac_fortune, lucky_number, fortune_cookie

def test_combined_functionality():
    name = "TestUser"
    lucky_num = lucky_number(name)
    zodiac = "Aries"
    
    assert isinstance(lucky_num, int)
    assert isinstance(zodiac_fortune(zodiac), str)
    assert isinstance(fortune_cookie(lucky=(lucky_num > 50)), str)