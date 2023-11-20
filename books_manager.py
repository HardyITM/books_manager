"""Модуль `sqlite3` предоставляет интерфейс для работы с SQLite."""
import sqlite3


class BookManager:
    """
    Класс для управления книгами в базе данных.
    """

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_books_table()
        self.create_genres_table()

    def create_books_table(self):
        """
        Создание таблицы 'books' в базе данных, если она не существует.
        """
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    description TEXT NOT NULL,
                    genre_id INTEGER NOT NULL,
                    FOREIGN KEY (genre_id) REFERENCES genres(id)
                )
            """)

    def create_genres_table(self):
        """
        Создание таблицы 'genres' в базе данных, если она не существует.
        """
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS genres (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """)

    def add_genre(self, name: str):
        """Добавление жанра

        Args:
            name (str): Название жанра
        """
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO genres (name) VALUES (?)", (name,))
            return cur.lastrowid

    def get_genres(self):
        """Получение всех существующих жанров

        Returns:
            genres (list): Список жанров
        """
        with self.conn:
            cursor = self.conn.execute("SELECT id, name FROM genres")
            genres = cursor.fetchall()
            return genres

    def add_book(
            self,
            title: str,
            author: str,
            description: str,
            genre_id: int
            ):
        """Добавление книги
        Args:
            title (str): Название
            author (str): Автор
            description (str): Описание
            genre_id (int): Айди жанра
        """
        with self.conn:
            self.conn.execute("""
                INSERT INTO books (
                    title, author, description, genre_id
                )
                VALUES (?, ?, ?, ?)""", (title, author, description, genre_id))

    def view_books_by_genre(self, genre=None):
        """Просмотр книг по жанру

        Args:
            genre (str, optional): Название жанра.

        Returns:
            books (list): Список книг
        """
        with self.conn:
            if genre:
                cursor = self.conn.execute("""
                    SELECT books.id, books.title, books.author
                    FROM books
                    INNER JOIN genres ON books.genre_id = genres.id
                    WHERE genres.name = ?
                    """, (genre,))
            else:
                cursor = self.conn.execute(
                    "SELECT id, title, author FROM books"
                    )
            books = cursor.fetchall()
            return books

    def search_books(self, keyword: str):
        """Поиск книги по названию или автору

        Args:
            keyword (str): Ключевое слово

        Returns:
            matching_books (list): Список найденных книг
        """
        with self.conn:
            cursor = self.conn.execute("""
                    SELECT id, title, author
                    FROM books
                    WHERE title LIKE ? OR author LIKE ?
                """, (f"%{keyword}%", f"%{keyword}%"))
            matching_books = cursor.fetchall()
            return matching_books

    def delete_book(self, book_id: int):
        """Удаление книги

        Args:
            book_id (int): Айди книги
        """
        with self.conn:
            self.conn.execute("DELETE FROM books WHERE id = ?", (book_id,))

    def get_book_details(self, book_id: int):
        """Подробная информация книги

        Args:
            book_id (int): Айди книги

        Returns:
            book_details (list): Описание книги
        """
        with self.conn:
            cursor = self.conn.execute("""
                    SELECT b.title, b.author, b.description, g.name AS genre
                    FROM books AS b
                    JOIN genres AS g ON b.genre_id = g.id
                    WHERE b.id = ?
                """, (book_id,))
            book_details = cursor.fetchone()
            return book_details
