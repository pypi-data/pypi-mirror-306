import pytest 
from pyquotes.quote_from_category import list_quote_from_category

sample_data = {
    "inspirational": [
        {"quote": "Life is like a box of chocolates.", "movie": "Forrest Gump"},
        {"quote": "Carpe diem. Seize the day.", "movie": "Dead Poets Society"},
    ],
    "sad": [
        {"quote": "I'll never let go, Jack.", "movie": "Titanic"},
        {"quote": "Why do fireflies have to die so soon?", "movie": "Grave of the Fireflies"},
    ],
}

def test_single_result(monkeypatch):
    monkeypatch.setattr("quotes.quote_categories", sample_data)
    result = list_quote_from_category("Titanic")
    assert result == ['"I\'ll never let go, Jack." - Sad']

def test_multiple_result(monkeypatch):
    sample_data["inspirational"].append(
        {"quote": "Stupid is as stupid does.", "movie": "Forrest Gump"}
    )
    monkeypatch.setattr("quotes.quote_categories", sample_data)
    result = list_quote_from_category("Forrest Gump")
    assert '"Life is like a box of chocolates." - Inspirational' in result
    assert '"Stupid is as stupid does." - Inspirational' in result

def test_no_results(monkeypatch):
    monkeypatch.setattr("quotes.quote_categories", sample_data)
    result = list_quote_from_category("Nonexistent Movie")
    assert result == ['There are currently no quotes from this movie, sorry!']