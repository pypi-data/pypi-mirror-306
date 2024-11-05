from pyquotes.list_movies import list_movies
def test_list_movies_returns_list():
    movies = list_movies()
    print(movies)
    assert isinstance(movies, list), "function should return a list of movies"
    assert len(movies) > 0, "The list shouldn't be empty"