import pytest
from funky_fortune.main import magic_8ball

def test_magic_8ball():
    question = "Will I become rich today?"
    answer = magic_8ball(question)
    assert question in answer
    assert any(response in answer for response in [
        "It is certain", "It is decidedly so", "Without a doubt",
        "You may rely on it", "My reply is no", "Better not tell you now",
        "Outlook not so good", "Cannot predict now"
    ])

def test_magic_8ball_empty_question():
    result = magic_8ball("")
    assert result.startswith("Question: ")
    assert "\nAnswer: " in result

def test_magic_8ball_long_question():
    long_question = "Why " * 100
    result = magic_8ball(long_question)
    assert result.startswith("Question: ")
    assert "\nAnswer: " in result

def test_magic_8ball_special_chars():
    special_question = "Will I win $1,000,000 tomorrow?!?!?"
    result = magic_8ball(special_question)
    assert special_question in result
    assert "\nAnswer: " in result

def test_magic_8ball_response_distribution():
    responses = set()
    for _ in range(100):
        result = magic_8ball("Test question")
        response = result.split("\nAnswer: ")[1]
        responses.add(response)
    assert len(responses) > 4  # Should get multiple different responses