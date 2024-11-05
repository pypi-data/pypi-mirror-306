from .quotes import inspirational, iconic, sad, funny

def list_movies():
    movies = set()
    for categories in [inspirational, sad, funny, iconic]:
        for quote in categories:
            movies.add(quote["movie"])
    return sorted(movies)
