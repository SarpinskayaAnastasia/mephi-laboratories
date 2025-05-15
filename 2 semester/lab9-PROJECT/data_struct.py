import functools
from hash_table.hash_table import HashTable
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


class Author:
    def __init__(self):
        self.name = ""
        self.second_name = ""
        self.patronymic = ""


class Book:
    def __init__(self):
        self.isbn = ""
        self.name = ""
        self.author = Author()
        self.year = 0
        self.genre = 0
        self.available = True


class Library:
    def __init__(self):
        """Хэш-функция показала не очень хорошие результаты для таблицы размером 10
         => берем сразу таблицу размером 100"""
        self.bookshelf = HashTable(100)

    @staticmethod
    def is_empty(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> R:
            if not len(self.bookshelf):
                raise IndexError("Bookshelf is empty. Type \"updata [FILE_PATH]\" or "
                                 "\"add [FILE_PATH]\" to add some books in library.")
            return func(self, *args, **kwargs)

        return wrapper

    @is_empty
    def find_book(self, isbn: str) -> Book:
        return self.bookshelf.get_value(isbn)

    def add_book(self, filepath: str):
        pass

    @is_empty
    def delete_book(self, isbn: str):
        pass

    def give_book(self, isbn: str):
        book_to_give = self.find_book(isbn)
        if book_to_give.available:
            book_to_give.available = False
            return
        raise ValueError("Book is unavailable")  # надо в дальнейшем прописать кастомные ошибки

    def receive_book(self, isbn: str):
        book_to_receive = self.find_book(isbn)
        if not book_to_receive.available:
            book_to_receive.available = True
            return
        raise ValueError("Book is already available")  # то же самое

    def load_from_file(self, filepath: str):
        pass

    def save_to_file(self, filepath: str):
        pass
