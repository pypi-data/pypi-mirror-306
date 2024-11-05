from pymovies import quotes
import random

def randomQuote():
    categories = []
    for category in dir(quotes):
        if isinstance(getattr(quotes, category), list) and getattr(quotes, category):
            categories.append(category)
    if not categories:
        return None 
    category = random.choice(categories)
    quote_info = random.choice(getattr(quotes, category))
    output = f"{quote_info['quote']} -- {quote_info['movie']} ({category})"
    return output