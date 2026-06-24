import pytest
import sqlite3
from src.db.movie_db import MovieDB

@pytest.fixture
def connect():
    db = MovieDB()
    yield db
    db.close()

def test_create_movie(connect: MovieDB):
    id = connect.create_movie("Пять ночей с Фредди", 2023, 8.5, "Хоррор")
    movie = connect.get_movie_by_id(id)

    assert movie is not None
    assert movie.id == 1
    assert movie.title == "Пять ночей с Фредди"
    assert movie.year == 2023
    assert movie.rating == 8.5
    assert movie.genre == "Хоррор"

def test_edit_move(connect: MovieDB):
    id = connect.create_movie("Майн фильм", 2225, 50.6, "Приключение")
    assert connect.update_movie(id, "Майнкрафт фильм", 2025, 5.6, "Приключение") == True
    movie = connect.get_movie_by_id(id)

    assert movie is not None
    assert movie.id == 1
    assert movie.title == "Майнкрафт фильм"
    assert movie.year == 2025
    assert movie.rating == 5.6
    assert movie.genre == "Приключение"

def test_delete_movie(connect: MovieDB):
    id = connect.create_movie("Пять ночей с Фредди", 2023, 8.5, "Хоррор")
    movie = connect.get_movie_by_id(id)

    assert movie is not None
    assert movie.id == 1
    assert movie.title == "Пять ночей с Фредди"
    assert movie.year == 2023
    assert movie.rating == 8.5
    assert movie.genre == "Хоррор"
    assert connect.delete_movie(id) == True
    assert connect.get_movie_by_id(id) is None

def test_genre_filter(connect: MovieDB):
    connect.create_movie("1", 2020, 8.0, "Хоррор")
    connect.create_movie("2", 2021, 7.5, "Комедия")
    connect.create_movie("3", 2022, 9.0, "Хоррор")

    horrors = connect.get_movies(genre="Хоррор")

    assert len(horrors) == 2
    assert horrors[0].title == "1"
    assert horrors[1].title == "3"


def test_year_sort(connect: MovieDB):
    connect.create_movie("1", 1999, 8.0, "Драма")
    connect.create_movie("2", 2025, 9.0, "Фантастика")
    connect.create_movie("3", 2015, 7.5, "Комедия")

    movies = connect.get_movies(year_sort=True)

    assert len(movies) == 3
    assert movies[0].year == 1999
    assert movies[1].year == 2015
    assert movies[2].year == 2025