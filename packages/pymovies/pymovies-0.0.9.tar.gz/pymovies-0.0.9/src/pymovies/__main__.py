import pymovies.list_movies
import pymovies.quote_from_category
import pymovies.quote_of_the_day
import pymovies.random_quote

def main():
    print(r"""
                                           |
                                ___________I____________
                               ( _____________________ ()
                              _.-'|                    ||
                          _.-'   ||      WELCOME       ||
         ______       _.-'       ||                    ||
        |      |_ _.-'           ||        TO          ||
        |      |_|_              ||                    ||
        |______|   `-._          ||      PYQUOTES      ||
           /\          `-._      ||                    ||
          /  \             `-._  ||         <3         ||
         /    \                `-.I____________________||
        /      \                 ------------------------
       /________\___________________/________________\______

    """)
    print(r"""
                    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                   ░░                          ░░
                  ░░     🎥  NOW SHOWING!      ░░
                   ░░                          ░░
                    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░

    Select an option:
    ──────────────────────────────────────────────────────
    🎞️  [1] View all movies
    🎲 [2] Get a random quote
    🎬 [3] Get a quote from a specific Movie
    ⭐ [4] Get the quote of the day
    ──────────────────────────────────────────────────────
    """)

    choice = input("Enter the number of your choice: ")

    if choice == "1":
        print("\n🍿 Movie List:")
        categories = pymovies.list_movies.list_movies()
        for category in categories:
            print(f"  🎥 {category}")
    elif choice == "2":
        quote = pymovies.random_quote.randomQuote()
        print(f"\n🎬 Random Quote:\n   \"{quote}\"")
    elif choice == "3":
        category = input("Enter Movie: ")
        try:
            quote = pymovies.quote_from_category.list_quote_from_category(category)
            print(f"\n🎥 Quote from {category}:\n   \"{quote}\"")
        except ValueError as e:
            print(f"\n🚫 {e}")
    elif choice == "4":
        quote_of_the_day = pymovies.quote_of_the_day.get_quote_of_the_day()
        print(f"\n⭐ Quote of the Day:\n   \"{quote_of_the_day}\"")
    else:
        print("\n⚠️ Invalid choice. Please enter a number from 1 to 4.")


if __name__ == "__main__":
    main()