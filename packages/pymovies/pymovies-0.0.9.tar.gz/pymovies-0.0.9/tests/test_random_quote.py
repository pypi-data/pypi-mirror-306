import pytest
from pyquotes import random_quote
import re

sample_data = {
    "inspirational": [
        {"quote": "Life is like a box of chocolates. You never know what you're gonna get.", "movie": "Forrest Gump"},
        {"quote": "Carpe diem. Seize the day, boys. Make your lives extraordinary.", "movie": "Dead Poets Society"},
    ],

    "sad": [
        {"quote": "I'll never let go, Jack. I promise.", "movie": "Titanic"},
        {"quote": "We all lose our loved ones. It’s part of life.", "movie": "A Walk to Remember"},
    ],

    "funny": [
        {"quote": "I'm not arguing, I'm just explaining why I'm right.", "movie": "The Office (TV Series)"},
        {"quote": "I’m not bad. I’m just drawn that way.", "movie": "Who Framed Roger Rabbit"},
    ],

    "iconic": [
        {"quote": "Why so serious?", "movie": "The Dark Knight"},
        {"quote": "To be or not to be, that is the question.", "movie": "Hamlet"},
    ]
}

def test_output_string(monkeypatch):
    monkeypatch.setattr("pyquotes.quotes", sample_data)
    for i in range(100):
            actual = random_quote.randomQuote()
            assert isinstance(
                actual, str
            ), f"Expected randomQuote() to return a string. Instead, it returned {actual}"
            assert (
                len(actual) > 0
            ), f"Expected randomQuote() not to be empty. Instead, it returned a string with {len(actual)} characters"

def test_output_structure(monkeypatch):
    monkeypatch.setattr("pyquotes.quotes", sample_data)
    expected_pattern = r'^"?(.+)"? -- .+ \(.+\)$'
    for i in range(100):
        actual = random_quote.randomQuote()
        assert re.match(expected_pattern, actual
        ), f"Expected randomQuote() structure to be {expected_pattern}. Instead, it returned {actual}"

def test_empty_categories(monkeypatch):
    monkeypatch.setattr("pyquotes.quotes.inspirational", [])
    monkeypatch.setattr("pyquotes.quotes.sad", [])
    monkeypatch.setattr("pyquotes.quotes.funny", [])
    monkeypatch.setattr("pyquotes.quotes.iconic", [])
    actual = random_quote.randomQuote()
    assert actual is None, f"Expected randomQuote() to return None. Instead, it returned {actual}"