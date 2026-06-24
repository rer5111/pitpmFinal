import pytest
from src.db.movie_db import MovieDB
from src.menu import handle_input

@pytest.fixture
def db():
    movie_database = MovieDB()
    yield movie_database
    movie_database.close()

def test_menu_show_all_empty(db):
    status, message, movies = handle_input("1", db)
    assert status == 0
    assert message == ""
    assert movies == [] 

def test_menu_add_movie_success(db):
    status, message, extra = handle_input(
        "2", db, title="Матрица", year="1999", rating="8.7", genre="Фантастика"
    )
    assert status == 0
    assert "Фильм добавлен с ID:" in message
    assert extra is None

def test_menu_add_movie_invalid_data(db):
    status, message, extra = handle_input(
        "2", db, title="Матрица", year="не_число", rating="8.7", genre="Фантастика"
    )
    assert status == 1
    assert message == "Неверный ввод!"
    assert extra is None

def test_menu_edit_movie_not_found(db):
    status, message, extra = handle_input(
        "3", db, id="999", title="Новое название", year="2020", rating="9.0", genre="Драма"
    )
    assert status == 1
    assert message == "Фильм с таким ID не найден!"
    assert extra is None

def test_menu_delete_movie_not_found(db):
    status, message, extra = handle_input("4", db, id="999")
    assert status == 1
    assert message == "Фильм с таким ID не найден!"
    assert extra is None

def test_menu_delete_movie_invalid_id(db):
    status, message, extra = handle_input("4", db, id="удалить_это")
    assert status == 1
    assert "ID должен быть числом" in message
    assert extra is None

def test_menu_filter_by_genre(db):
    db.create_movie("Фильм 1", 2020, 8.0, "Хоррор")
    db.create_movie("Фильм 2", 2021, 7.0, "Комедия")
    
    status, message, movies = handle_input("5", db, genre="Хоррор")
    assert status == 0
    assert "Фильтрация по жанру" in message
    assert len(movies) == 1
    assert movies[0].title == "Фильм 1"

def test_menu_sort_by_year(db):
    db.create_movie("Новый", 2025, 9.0, "Экшен")
    db.create_movie("Старый", 1999, 8.0, "Экшен")
    
    status, message, movies = handle_input("6", db)
    assert status == 0
    assert message == "Сортировка по году выпуска"
    assert len(movies) == 2
    assert movies[0].year == 1999

def test_menu_exit(db):
    status, message, extra = handle_input("0", db)
    assert status == -1
    assert message == "До свидания!"
    assert extra is None

def test_menu_unknown_function(db):
    status, message, extra = handle_input("99", db)
    assert status == 1
    assert message == "Данная функция отсутствует в меню."
    assert extra is None

def test_menu_empty_string(db):
    status, message, extra = handle_input("2", db, title="", year=2020, rating=10, genre="")
    assert status == 1
    assert message == "Нельзя добавить пустое значение."
    assert extra is None

def test_menu_wrong_rating(db):
    status, message, extra = handle_input("2", db, title="1", year=2020, rating=12, genre="genre")
    assert status == 1
    assert message == "Введите рейтинг от 0 до 10"
    assert extra is None