import pytest
from src.db.movie_db import MovieDB
from src.menu import handle_input

@pytest.fixture
def db():
    movie_database = MovieDB(":memory:")
    yield movie_database
    movie_database.close()

def test_edge_case_delete_non_existent_id(db):
    status, message, extra = handle_input("4", db, id="99999")
    assert status == 1
    assert "не найден" in message.lower()
    assert extra is None

def test_edge_case_update_non_existent_id(db):
    status, message, extra = handle_input(
        "3", db, id="88888", title="Тест", year="2026", rating="5.5", genre="Драма"
    )
    assert status == 1
    assert "не найден" in message.lower()
    assert extra is None

def test_edge_case_invalid_menu_choice(db):
    status, message, extra = handle_input("abc", db)
    assert status == 1
    assert "отсутствует" in message.lower()
    assert extra is None
