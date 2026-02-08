import os

import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
API_KEY = os.getenv("API_KEY")

# Define the database URL
DB_URL = "sqlite:///data/movies.db"
OMDB_URL = "http://www.omdbapi.com/"


# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(
        text(
            """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT NOT NULL
        )
    """
        )
    )
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
        movies = result.fetchall()

    return {
        row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies
    }


def add_movie(title):
    """Add a new movie to the database."""
    params = {"apikey": API_KEY, "t": title}
    try:
        print("starting request")
        movie_info = requests.get(OMDB_URL, params=params)
        print(type(movie_info))
        print(movie_info)
    except Exception as e:
        print(f"Error. {e}")
    else:
        movie_info = movie_info.json()
        if movie_info["Response"] == "False":
            print(f"Error: {movie_info['Error']}")
            return

        title_api = movie_info["Title"]
        year = movie_info["Year"]
        rating = movie_info["imdbRating"]
        poster_url = movie_info["Poster"]

        with engine.connect() as connection:
            try:
                connection.execute(
                    text(
                        "INSERT INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating, :poster)"
                    ),
                    {
                        "title": title_api,
                        "year": year,
                        "rating": rating,
                        "poster": poster_url,
                    },
                )
                connection.commit()
                print(f"Movie '{title_api}' added successfully.")
            except Exception as e:
                print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("DELETE FROM movies WHERE title = :title"), {"title": title}
            )
            connection.commit()
            print(f"Movie {title} deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("UPDATE movies SET rating = :rating WHERE title = :title"),
                {"title": title, "rating": rating},
            )
            connection.commit()
            print(f"Movie {title} updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
