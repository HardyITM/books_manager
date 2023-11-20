"""Модуль `NoteManager` предоставляет функционал для управления книгами."""
from books_manager import BookManager


def main():
    """
    Основная функция для взаимодействия с менеджером книг.

    Она представляет меню пользователю с различными опциями для управления
    книгами, включая добавление, просмотр, поиск, удаление
    и просмотр подробной информации о книгах.
    """
    db_name = "books.db"
    book_manager = BookManager(db_name)

    while True:
        print_menu()
        choice = input("Введите номер действия: ")
        choices = {
            '1': add_book,
            '2': view_all_books,
            '3': search_books,
            '4': delete_book,
            '5': view_book_details,
        }
        if choice in choices:
            print(choices[choice](book_manager))
        elif choice == '6':
            break
        else:
            print("Неправильный выбор. Выберите существующий номер действия.")


def print_menu():
    """
    Выводит на экран меню с возможными действиями для управления книгами.
    """
    print("Меню:")
    print("1. Добавить новую книгу")
    print("2. Просмотреть список книг")
    print("3. Поиск книг по ключевому слову")
    print("4. Удалить книгу")
    print("5. Просмотреть подробную информацию о книге")
    print("6. Выйти")


def add_book(book_manager: BookManager):
    """Добавление книги

    Args:
        book_manager (BookManager): Класс управления базой книг

    Returns:
        text (str): Конечный текст
    """
    title = input("Введите название книги: ")
    author = input("Введите имя автора книги: ")
    description = input("Введите описание книги: ")
    genres = book_manager.get_genres()
    if not genres:
        print('Список жанров пуст')
    else:
        for i, genre in enumerate(genres, 1):
            print(f"{i}. {genre[1]}")

    print("Если жанра нет или список пуст, введите название нового жанра")

    genre_choice = input("Введите номер жанра или название нового жанра: ")

    if not genre_choice.isdigit():
        genre_id = book_manager.add_genre(genre_choice)
    else:
        genre_choice = int(genre_choice)
        if 1 > genre_choice or genre_choice > len(genres):
            return "Несуществующий номер жанра. Попробуйте снова."
        genre_id = genres[genre_choice - 1][0]

    book_manager.add_book(title, author, description, genre_id)
    return "Книга успешно добавлена!"


def view_all_books(book_manager: BookManager):
    """Просмотр всех книг

    Args:
        book_manager (BookManager): Класс управления базой книг
    Returns:
        text (str): Конечный текст
    """
    text = (
        "Если хотите получить книги с определенным жанром, введите его\n"
        "Иначе просто нажмите Enter"
    )
    print(text)
    choice = input('Жанр: ')
    books = book_manager.view_books_by_genre(choice)
    if not books:
        return 'Книги отсутствуют'
    all_books = [f"{book[0]}. {book[1]} by {book[2]}" for book in books]
    return "\n".join(all_books)


def search_books(book_manager: BookManager):
    """Просмотр всех найденных книг

    Args:
        book_manager (BookManager): Класс управления базой книг
    Returns:
        text (str): Конечный текст
    """
    keyword = input("Введите ключевое слово для поиска: ")
    matching_books = book_manager.search_books(keyword)
    if not matching_books:
        return "Книги с заданным ключевым словом не найдены."
    print("Найденные книги:")
    books = [f"{book[0]}. {book[1]} by {book[2]}" for book in matching_books]
    return "\n".join(books)


def delete_book(book_manager: BookManager):
    """Удаление книги

    Args:
        book_manager (BookManager): Класс управления базой книг
    Returns:
        text (str): Конечный текст
    """
    book_id = input("Введите номер книги для удаления: ")
    if not book_id.isdigit():
        return "Неправильный номер книги, возможно вы ввели не число."
    book_manager.delete_book(int(book_id))
    return "Книга успешно удалена!"


def view_book_details(book_manager: BookManager):
    """Просмотр всех книг

    Args:
        book_manager (BookManager): Класс управления базой книг
    Returns:
        text (str): Конечный текст
    """
    book_id = input("Введите номер книги для просмотра подробной информации: ")
    if not book_id.isdigit():
        return "Неправильный номер книги, возможно вы ввели не число."
    book = book_manager.get_book_details(int(book_id))
    if not book:
        return "Книга с указанным номером не найдена."
    book_info = [
        f"Название: {book[0]}",
        f"Автор: {book[1]}",
        f"Описание: {book[2]}",
        f"Жанр: {book[3]}"
        ]
    return "\n".join(book_info)


if __name__ == "__main__":
    main()
