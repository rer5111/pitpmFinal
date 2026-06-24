from src.db.movie_db import MovieDB

def handle_input(inp: str, db: MovieDB, **data) -> dict:
    if inp == "1":
        movies = db.get_movies()
        return (0, "", movies)
        
    elif inp == "2":
        try:
            title = data.get("title")
            year = int(data.get("year"))
            rating = float(data.get("rating"))
            genre = data.get("genre")
            if title == "" or genre == "":
                return (1, "Нельзя добавить пустое значение.", None)
            if not 0 <= rating <= 10:
                return (1, "Введите рейтинг от 0 до 10", None)
            movie_id = db.create_movie(title, year, rating, genre)
            return (0, f"Фильм добавлен с ID: {movie_id}", None)
        except (ValueError, TypeError):
            return (1, "Неверный ввод!", None)
            
    elif inp == "3":
        try:
            movie_id = int(data.get("id"))
            title = data.get("title")
            year = int(data.get("year"))
            rating = float(data.get("rating"))
            genre = data.get("genre")
            if title == "" or genre == "":
                return (1, "Нельзя добавить пустое значение.", None)
            if not 0 <= rating <= 10:
                return (1, "Введите рейтинг от 0 до 10", None)
            if db.update_movie(movie_id, title, year, rating, genre):
                return (0, "Фильм успешно обновлен!", None)
            return (1, "Фильм с таким ID не найден!", None)
        except (ValueError, TypeError):
            return (1, "Ошибка: Неверный ввод!", None)
            
    elif inp == "4":
        try:
            movie_id = int(data.get("id"))
            if db.delete_movie(movie_id):
                return (0, "Фильм успешно удален!", None)
            return (1, "Фильм с таким ID не найден!", None)
        except (ValueError, TypeError):
            return (1, "Ошибка: ID должен быть числом!", None)
            
    elif inp == "5":
        genre = data.get("genre")
        movies = db.get_movies(genre=genre)
        return (0, f"Фильтрация по жанру '{genre}'", movies)
        
    elif inp == "6":
        movies = db.get_movies(year_sort=True)
        return (0, "Сортировка по году выпуска", movies)
    
    elif inp == "7":
        movies = db.get_movies(year_sort=False)
        return (0, "Сортировка по году выпуска", movies)
    
    elif inp == "8":
        movies = db.get_movies()
        out = []
        try:
            for m in movies:
                if data.get("before"):
                    if m.year < int(data.get("year")):
                        out.append(m)
                else:
                    if m.year > int(data.get("year")):
                        out.append(m)
        except:
            return(1, "Введено неправильное значение", None)
        return (0, "Фильтрация по году", out)
    elif inp == "0":
        return (-1, "До свидания!", None)
        
    return (1, "Данная функция отсутствует в меню.", None)

def print_movies_table(movies: list):
    if not movies:
        print("\nФильмов нет.")
        return
    print(f"\n{'ID':<5} | {'Название':<25} | {'Год':<6} | {'Рейтинг':<7} | {'Жанр':<15}")
    print("-" * 70)
    for m in movies:
        print(f"{m.id:<5} | {m.title:<25} | {m.year:<6} | {m.rating:<7} | {m.genre:<15}")
