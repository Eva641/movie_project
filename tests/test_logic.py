import unittest
import json
import os
import tempfile
from logic import load_movies, save_movies, add_movie, mark_watched, find_by_year


class TestMovieCatalog(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.test_data = [
            {"id": 1, "title": "The Matrix", "year": 1999, "watched": False},
            {"id": 2, "title": "Inception", "year": 2010, "watched": True}
        ]

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_load_movies_existing_file(self):
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            json.dump(self.test_data, f)

        movies = load_movies(self.temp_file.name)
        self.assertEqual(len(movies), 2)
        self.assertEqual(movies[0]['title'], "The Matrix")

    def test_load_movies_non_existing_file(self):
        movies = load_movies("non_existing_file.json")
        self.assertEqual(movies, [])

    def test_add_movie(self):
        movies = []
        movies = add_movie(movies, "Test Movie", 2023)

        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]['title'], "Test Movie")
        self.assertEqual(movies[0]['year'], 2023)
        self.assertEqual(movies[0]['id'], 1)
        self.assertFalse(movies[0]['watched'])

        movies = add_movie(movies, "Another Movie", 2024)
        self.assertEqual(len(movies), 2)
        self.assertEqual(movies[1]['id'], 2)

    def test_mark_watched_existing_id(self):
        movies = self.test_data.copy()
        updated_movies = mark_watched(movies, 1)

        movie_1 = next(m for m in updated_movies if m['id'] == 1)
        self.assertTrue(movie_1['watched'])

        movie_2 = next(m for m in updated_movies if m['id'] == 2)
        self.assertTrue(movie_2['watched'])

    def test_mark_watched_non_existing_id(self):
        movies = self.test_data.copy()
        original_length = len(movies)

        updated_movies = mark_watched(movies, 999)

        self.assertEqual(len(updated_movies), original_length)

    def test_find_by_year(self):
        movies = self.test_data.copy()

        found = find_by_year(movies, 1999)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]['title'], "The Matrix")

        found = find_by_year(movies, 2000)
        self.assertEqual(len(found), 0)

    def test_save_movies(self):
        save_movies(self.temp_file.name, self.test_data)


        self.assertTrue(os.path.exists(self.temp_file.name))

        with open(self.temp_file.name, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        self.assertEqual(loaded_data, self.test_data)


if __name__ == '__main__':
    unittest.main()