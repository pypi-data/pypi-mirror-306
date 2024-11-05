import pytest
from pyquotes.quote_of_the_day import get_quote_of_the_day
import datetime
import random

# test that there is an output
def test_get_quote_of_the_day_no_empty_quotes():
    """Test that the quote of the day is never empty."""
    output = get_quote_of_the_day()
    assert output.strip() != "", "Output should not be empty"
    
# test if a string is returned
def test_get_quote_of_the_day_returns_string():
        quote = get_quote_of_the_day()
        assert isinstance(quote, str), "Quote of the Day should be a string"
        assert len(quote) > 0, "Quote of the Day should not be empty"
        assert " - " in quote, "Quote should include the movie name"

# test if the date is in the output
def test_get_quote_of_the_day_prints_today():
        today = datetime.date.today()
        output = get_quote_of_the_day()
        assert str(today) in output, f"Expected date {today} not found in output: {output}"