import os
from src.db.movie_db import MovieDB
from src.menu import handle_input, print_movies_table

def show_ui_menu():
    print("\nБИБЛИОТЕКА ФИЛЬМОВ")
    print("1. Показать все фильмы")
    print("2. Добавить новый фильм")
    print("3. Редактировать фильм")
    print("4. Удалить фильм")
    print("5. Фильтрация по жанру")
    print("6. Сортировка по году выпуска")
    print("7. Обратная сортировка по году выпуска")
    print("0. Выход")

def main():
    db = MovieDB("db.db")
    
    try:
        while True:
            show_ui_menu()
            choice = input("\nВыберите действие: ").strip()
            
            # Собираем аргументы для отправки в зависимости от выбора
            data = {}
            if choice == "2":
                data["title"] = input("Название: ").strip()
                data["year"] = input("Год: ").strip()
                data["rating"] = input("Рейтинг: ").strip()
                data["genre"] = input("Жанр: ").strip()
            elif choice == "3":
                data["id"] = input("ID фильма для редактирования: ").strip()
                data["title"] = input("Новое название: ").strip()
                data["year"] = input("Новый год: ").strip()
                data["rating"] = input("Новый рейтинг: ").strip()
                data["genre"] = input("Новый жанр: ").strip()
            elif choice == "4":
                data["id"] = input("ID фильма для удаления: ").strip()
            elif choice == "5":
                data["genre"] = input("Введите жанр для фильтрации: ").strip()
            
            # Отправляем данные на обработку в меню
            status, message, extra = handle_input(choice, db, **data)
            
            # Выводим текстовый ответ, если он есть
            if message:
                print(message)
                
            # Если вернулись данные (список фильмов), выводим их
            if extra is not None:
                print_movies_table(extra)
                
            # Если статус exit — выходим из бесконечного цикла
            if status == -1:
                break
                
    finally:
        db.close()

if __name__ == "__main__":
    main()
