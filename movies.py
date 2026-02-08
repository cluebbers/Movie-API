import os
import random
import sys
from statistics import mean, median

import matplotlib.pyplot as plt
import movie_storage.movie_storage_sql as storage
from colorama import Fore, Style
from movie_web_generator import load_template, serialize_movies, write_output

CURRENT_YEAR = 2025


def print_menu():
    """prints the menu and returns the user choice

    Returns:
        string: use rinput choice
    """
    print(Fore.GREEN + "\nMenu:")
    print("0. Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print("9. Movies sorted by year")
    print("10. Filter Movies")
    print("11. Create Rating Histogram")
    print("12. Generate website")
    user_choice = input(Fore.YELLOW + "\nEnter choice (0-12): " + Style.RESET_ALL)
    print("")

    return user_choice


def exit_program():
    """program exits"""
    print(Fore.GREEN + "Bye!" + Style.RESET_ALL)
    sys.exit()


def list_movies(movies=None):
    """lists all movies in the database

    Args:
        movies (dict of dict): dictionary of movies
    """
    if movies is None:
        movies = storage.list_movies()
    total_movies = len(movies)
    print(Fore.GREEN + f"{total_movies} movies in total")
    for movie in movies:
        print(f"{movie} ({movies[movie]['year']}): {movies[movie]['rating']}")


def verify_rating(rating):
    """sets a rating for a movie

    Returns:
        float: rating between 0 and 10
    """
    while True:
        try:
            rating = float(rating)
            if 0 <= rating <= 10:
                return rating
            print(Fore.RED + "Rating must be between 0 and 10!" + Style.RESET_ALL)
            rating = input()
        except ValueError:
            print(
                Fore.RED
                + "Invalid input. Please enter a number between 0 and 10."
                + Style.RESET_ALL
            )
            rating = input()


def verify_year(year):
    """sets a year for a movie

    Returns:
        int: year below current year
    """
    while True:
        try:
            year = int(year)
            if year <= CURRENT_YEAR:
                return year
            print(
                Fore.RED
                + f"Year must be between under {CURRENT_YEAR}!"
                + Style.RESET_ALL
            )
            year = input()
        except ValueError:
            print(
                Fore.RED
                + "Invalid input. Please enter a valid year (YYYY)."
                + Style.RESET_ALL
            )
            year = input()


def add_movie():
    """adds a movie to the database

    Args:
        movies (dict of dict): dictionary of movies

    Returns:
        dict of dict: updated dictionary of movies
    """
    movies = storage.list_movies()
    new_movie_name = input(Fore.YELLOW + "Enter new movie name: " + Style.RESET_ALL)
    if new_movie_name in movies:
        print(Fore.RED + f"Movie {new_movie_name} already exist!")
    elif new_movie_name == "":
        print(Fore.RED + "Movie name cannot be empty!" + Style.RESET_ALL)
    else:
        # rating = float(
        #     input(Fore.YELLOW + "Enter movie rating (0 - 10): " + Style.RESET_ALL)
        # )
        # new_movie_rating = verify_rating(rating)
        # year = input(
        #     Fore.YELLOW + "Enter movie year (1888 - current year): " + Style.RESET_ALL
        # )
        # new_movie_year = verify_year(year)

        storage.add_movie(new_movie_name)#, new_movie_year, new_movie_rating)

        #print(Fore.GREEN + f"Movie {new_movie_name} has been successfully added")


def delete_movie():
    """deletes a movie from the database

    Args:
        movies (dict of dict): dictionary of movies

    Returns:
        dict of dict: updated dictionary of movies
    """
    movies = storage.list_movies()
    movie_to_delete = input(
        Fore.YELLOW + "Enter movie name to delete: " + Style.RESET_ALL
    )
    if movie_to_delete in movies:
        storage.delete_movie(movie_to_delete)
        print(
            Fore.GREEN
            + f"Movie {movie_to_delete} successfully deleted"
            + Style.RESET_ALL
        )
    else:
        print(Fore.RED + f"Movie {movie_to_delete} doesn't exist!" + Style.RESET_ALL)


def update_movie():
    """updates a movie in the database

    Args:
        movies (dict of dict): dictionary of movies

    Returns:
        dict of dict: updated dictionary of movies
    """
    movies = storage.list_movies()
    movie_to_update = input(Fore.YELLOW + "Enter movie name: " + Style.RESET_ALL)
    if movie_to_update in movies:
        new_rating = input(
            Fore.YELLOW + "Enter new movie rating (0 - 10): " + Style.RESET_ALL
        )
        new_rating = verify_rating(new_rating)
        storage.update_movie(movie_to_update, new_rating)
        print(
            Fore.GREEN
            + f"Movie {movie_to_update} successfully updated"
            + Style.RESET_ALL
        )
    else:
        print(Fore.RED + f"Movie {movie_to_update} doesn't exist!" + Style.RESET_ALL)


def movie_stats():
    """calculates statistics and prints them

    Args:
        movies (dict of dict): dictionary of movies
    """
    movies = storage.list_movies()

    if not movies:
        print(Fore.RED + "No movies in the database!" + Style.RESET_ALL)
        return

    all_ratings = []
    max_rating = 0
    min_rating = 10
    best_movie = []
    worst_movie = []

    for movie in movies:
        rating = movies[movie]["rating"]
        all_ratings.append(rating)

        if rating > max_rating:
            max_rating = rating
            best_movie = [movie]
        elif rating == max_rating:
            best_movie.append(movie)

        if rating < min_rating:
            min_rating = rating
            worst_movie = [movie]
        elif rating == min_rating:
            worst_movie.append(movie)

    average_rating = mean(all_ratings)
    median_rating = median(all_ratings)

    print(Fore.GREEN + f"Average rating: {average_rating:.1f}")
    print(f"Median rating: {median_rating}")
    print(
        f"Best movie(s): {', '.join(best_movie)}, rating: {movies[best_movie[0]]['rating']}"
    )
    print(
        f"Worst movie(s): {', '.join(worst_movie)}, rating: {movies[worst_movie[0]]['rating']}"
        + Style.RESET_ALL
    )


def random_movie():
    """prints a random movie from the database

    Args:
        movies (dict of dict): dictionary of movies
    """
    movies = storage.list_movies()
    movie = random.choice(list(movies.keys()))
    print(
        Fore.GREEN
        + f"Your movie for tonight: {movie}, it's rated {movies[movie]['rating']}"
        + Style.RESET_ALL
    )


def search_movie():
    """searches for a movie in the database

    Args:
        movies (dict of dict): dictionary of movies
    """
    movies = storage.list_movies()
    movie_to_search = input(
        Fore.YELLOW + "Enter part of movie name: " + Style.RESET_ALL
    ).lower()
    movies_found = False
    for movie in movies:
        if movie_to_search in movie.lower():
            print(
                Fore.GREEN
                + f"{movie} ({movies[movie]['year']}): {movies[movie]['rating']}"
                + Style.RESET_ALL
            )
            movies_found = True
    if not movies_found:
        print(Fore.RED + f"No movies found with {movie_to_search}" + Style.RESET_ALL)


def movies_by_rating():
    """prints movies sorted by rating

    Args:
        movies (dict of dict): dictionary of movies
    """
    movies = storage.list_movies()
    for title, info in sorted(
        movies.items(), key=lambda item: item[1]["rating"], reverse=True
    ):
        print(Fore.GREEN + f"{title}: {info['rating']}" + Style.RESET_ALL)


def chronological_movies():
    """asks how the user wants the list to be ordered

    Returns:
        bool: True if latest movies first, False otherwise
    """
    while True:
        movie_order = input(
            Fore.YELLOW
            + "Do you want the latest movies first? (Y/N) "
            + Style.RESET_ALL
        ).lower()
        if movie_order == "y":
            return True
        if movie_order == "n":
            return False
        print(Fore.RED + "Invalid input. Please enter 'Y' or 'N'." + Style.RESET_ALL)
        continue


def movies_by_year():
    """prints movies sorted by year

    Args:
        movies (dict of dict): dictionary of movies
    """
    reversed_order = chronological_movies()
    movies = storage.list_movies()
    for title, info in sorted(
        movies.items(), key=lambda item: item[1]["year"], reverse=reversed_order
    ):
        print(Fore.GREEN + f"{title}: {info['year']}" + Style.RESET_ALL)


def filter_movies():
    """filters movie by year and rating"""
    minimum_rating = input(
        Fore.YELLOW
        + "Enter minimum rating (leave blank for no minimum rating): "
        + Style.RESET_ALL
    )
    minimum_rating = verify_rating(minimum_rating) if minimum_rating else None
    start_year = input(
        Fore.YELLOW
        + "Enter start year (leave blank for no start year): "
        + Style.RESET_ALL
    )
    start_year = verify_year(start_year) if start_year else None
    end_year = input(
        Fore.YELLOW + "Enter end year (leave blank for no end year): " + Style.RESET_ALL
    )
    end_year = verify_year(end_year) if end_year else None
    movies = storage.list_movies()
    filtered_movies = {}
    for title, info in movies.items():
        if minimum_rating and info["rating"] < float(minimum_rating):
            continue
        if start_year and info["year"] < int(start_year):
            continue
        if end_year and info["year"] > int(end_year):
            continue
        filtered_movies[title] = info
    print(Fore.GREEN + "Filtered Movies:")
    list_movies(filtered_movies)
    print(Style.RESET_ALL)


def create_rating_histogram():
    """creates a histogram by rating and saves it to a file

    Args:
        movies (dict of dict): dictionary of movies
    """
    movies = storage.list_movies()
    user_filepath = input(
        Fore.YELLOW + "Enter filename to save the histogram: " + Style.RESET_ALL
    )
    ratings = [info["rating"] for info in movies.values()]
    plt.hist(ratings, bins=10, range=(0, 10))
    plt.xlabel("Rating")
    plt.ylabel("Number of Movies")
    plt.title("Movie Ratings Histogram")
    plt.savefig(user_filepath)
    plt.close()

def create_html():
    """write an html file according to the template and output

    Args:
        output (html): html with animal information
    """
    movies = storage.list_movies()
    output = ""
    for title, info in movies.items():
        movie_obj = {
            "title": title,
            "year": info["year"],
            "poster": info.get("poster", ""),
        }
        output += serialize_movies(movie_obj)
    template = load_template("_static/index_template.html")
    template = template.replace("__TEMPLATE_TITLE__", "My Movie App")
    template = template.replace("__TEMPLATE_MOVIE_GRID__", output)
    
    os.makedirs("output", exist_ok=True)
    with open("_static/style.css", "r") as src:
        css = src.read()
    with open("output/style.css", "w") as dst:
        dst.write(css)
        
    write_output("output/movies.html", template)

    print("Website was generated successfully.")
    
    
def main():
    """main function to run the program"""
    func_dict = {
        "0": exit_program,
        "1": list_movies,
        "2": add_movie,
        "3": delete_movie,
        "4": update_movie,
        "5": movie_stats,
        "6": random_movie,
        "7": search_movie,
        "8": movies_by_rating,
        "9": movies_by_year,
        "10": filter_movies,
        "11": create_rating_histogram,
        "12": create_html
    }

    print("********** My Movies Database **********")
    while True:
        user_choice = print_menu()
        if user_choice in func_dict:
            func_dict[user_choice]()
        else:
            print(Fore.RED + "Invalid choice" + Style.RESET_ALL)
            continue

        press_enter = input(Fore.YELLOW + "\nPress Enter to continue")
        if press_enter == "":
            continue


if __name__ == "__main__":
    main()
