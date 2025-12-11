from logic import *
import os

DATA_FILE = 'movies.json'


def display_movies(movies):

    if not movies:
        print("Каталог пуст.")
        return

    print("\n" + "=" * 50)
    print("СПИСОК ФИЛЬМОВ:")
    for movie in movies:
        status = "✓" if movie['watched'] else "✗"
        print(f"ID: {movie['id']} | {movie['title']} ({movie['year']}) | Просмотрен: {status}")
    print("=" * 50)


def show_all_movies(movies):

    display_movies(movies)


def add_new_movie(movies):

    print("\n--- ДОБАВЛЕНИЕ НОВОГО ФИЛЬМА ---")
    title = input("Введите название фильма: ").strip()

    if not title:
        print("Название не может быть пустым!")
        return movies

    try:
        year = int(input("Введите год выпуска: "))
        if year < 1888 or year > 2100:
            print("Введите корректный год!")
            return movies
    except ValueError:
        print("Год должен быть числом!")
        return movies

    movies = add_movie(movies, title, year)
    save_movies(DATA_FILE, movies)
    print(f"Фильм '{title}' ({year}) успешно добавлен!")
    return movies


def mark_as_watched(movies):

    display_movies(movies)

    if not movies:
        return movies

    try:
        movie_id = int(input("\nВведите ID фильма для отметки как просмотренный: "))
    except ValueError:
        print("ID должен быть числом!")
        return movies

    movies = mark_watched(movies, movie_id)
    save_movies(DATA_FILE, movies)


    found = any(movie['id'] == movie_id for movie in movies if movie['watched'])
    if found:
        print("Фильм отмечен как просмотренный!")
    else:
        print(f"Фильм с ID {movie_id} не найден.")

    return movies


def search_by_year(movies):

    try:
        year = int(input("Введите год для поиска: "))
    except ValueError:
        print("Год должен быть числом!")
        return

    found_movies = find_by_year(movies, year)

    if found_movies:
        print(f"\nНайдено фильмов за {year} год: {len(found_movies)}")
        display_movies(found_movies)
    else:
        print(f"Фильмов за {year} год не найдено.")


def main():

    print("=" * 50)
    print("КАТАЛОГ ФИЛЬМОВ")
    print("=" * 50)

    # Загружаем фильмы при старте
    movies = load_movies(DATA_FILE)

    while True:
        print("\n--- МЕНЮ ---")
        print("1. Показать все фильмы")
        print("2. Добавить фильм")
        print("3. Отметить фильм как просмотренный")
        print("4. Найти фильмы по году")
        print("0. Выход")

        choice = input("\nВыберите действие: ").strip()

        if choice == '0':
            print("Сохранение данных...")
            save_movies(DATA_FILE, movies)
            print("До свидания!")
            break

        elif choice == '1':
            show_all_movies(movies)

        elif choice == '2':
            movies = add_new_movie(movies)

        elif choice == '3':
            movies = mark_as_watched(movies)

        elif choice == '4':
            search_by_year(movies)

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()