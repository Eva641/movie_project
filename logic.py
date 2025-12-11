import json
from typing import List, Dict


def load_movies(path: str) -> List[Dict]:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            movies = json.load(file)
            return movies if isinstance(movies, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_movies(path: str, movies: List[Dict]) -> None:
    with open(path, 'w') as file:
        json.dump(movies, file, ensure_ascii=False, indent=2)


def add_movie(movies: List[Dict], title: str, year: int) -> List[Dict]:
    if not movies:
        new_id = 1
    else:
        new_id = max(movie.get('id', 0) for movie in movies) + 1

    new_movie = {
        'id': new_id,
        'title': title,
        'year': year,
        'watched': False
    }

    return movies + [new_movie]


def mark_watched(movies: List[Dict], movie_id: int) -> List[Dict]:

    updated_movies = []
    for movie in movies:
        if movie['id'] == movie_id:
            updated_movie = movie.copy()
            updated_movie['watched'] = True
            updated_movies.append(updated_movie)
        else:
            updated_movies.append(movie)

    return updated_movies

def find_by_year(movies: List[Dict], year: int) -> List[Dict]:

    return [movie for movie in movies if movie['year'] == year]