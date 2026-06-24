import sqlite3
from src.db.film_model import Movie

class MovieDB:
    def __init__(self, db_path=":memory:"):
        self.connection = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                genre TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def create_movie(self, title, year, rating, genre):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO movies (title, year, rating, genre) VALUES (?, ?, ?, ?)",
            (title, year, rating, genre)
        )
        self.connection.commit()
        return cursor.lastrowid
    
    def update_movie(self, id, title, year, rating, genre):
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE movies SET title=?, year=?, rating=?, genre=? WHERE id=?""", (title, year, rating, genre, id)
        )
        self.connection.commit()
        return cursor.rowcount > 0
    
    def delete_movie(self, id):
        cursor = self.connection.cursor()
        cursor.execute(
            """DELETE FROM movies WHERE id=?""", (id,)
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def get_movie_by_id(self, movie_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, title, year, rating, genre FROM movies WHERE id = ?", (movie_id,))
        row = cursor.fetchone()

        if row:
            return Movie.from_tuple(row)
        else: 
            return None
    
    def get_movies(self, genre = None, year_sort = None):
        cursor = self.connection.cursor()
        
        query = "SELECT id, title, year, rating, genre FROM movies"
        params = []

        if genre:
            query += " WHERE genre = ?"
            params.append(genre)

        if year_sort is not None:
            if year_sort:
                query += " ORDER BY year ASC"
            else:
                query += " ORDER BY year DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [Movie.from_tuple(row) for row in rows]

    def close(self):
        self.connection.close()