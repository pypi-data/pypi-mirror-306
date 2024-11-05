from .quotes import quote_categories
def list_quote_from_category(movie_name):
    results = []
    for category, quotes in quote_categories.items():
        for quote in quotes:
            if quote["movie"].lower() == movie_name.lower():
                results.append(f'"{quote["quote"]}" - {category.capitalize()}')
    if results:
        # print(f'Quotes from "{movie_name}":')
        # for quote in results:
        #     print(quote)
        return results
    else:
        print('There are currently no quotes from this movie, sorry!')

# list_quote_from_category("The Dark Knight")