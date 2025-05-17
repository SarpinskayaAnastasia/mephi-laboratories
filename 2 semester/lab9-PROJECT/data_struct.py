import functools
from hash_table.hash_table import HashTable
from typing import Callable, TypeVar, ParamSpec
from pathlib import Path
import csv

from tools import EmptyLibrary, IncorrectBookStatus, BookDoesntExist, check_isbn

P = ParamSpec("P")
R = TypeVar("R")


class Author:
    def __init__(self):
        self.name = ""
        self.second_name = ""
        self.patronymic = ""


class Book:
    def __init__(self, isbn: str):
        self.isbn = isbn
        self.name = ""
        self.author = Author()
        self.year = 0
        self.genre = ""
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
                raise EmptyLibrary()
            return func(self, *args, **kwargs)

        return wrapper

    @is_empty
    def find_book(self, isbn: str) -> Book:
        if not check_isbn(isbn):
            raise BookDoesntExist("Incorrect ISBN!")
        interesting_book = self.bookshelf.get_value(isbn)
        if not interesting_book:
            raise BookDoesntExist("The ISBN you entered doesn't match any book.")
        return interesting_book

    def add_book(self, filepath: str):
        fp = Path(filepath)
        if fp.exists():
            if fp.is_file():
                if fp.suffix.lower() == ".csv":
                    with fp.open("r", encoding="UTF-8") as new_book:
                        reader = csv.reader(new_book, delimiter=';')
                        try:
                            header = next(reader)
                        except StopIteration:
                            raise ValueError("File is empty!")
                        """мы хотим *.csv с таким заголовком:
                        ISBN;Book Name;Author Name;Author Second Name;Author Patronymic;Publishing Year;Genre;Status
                        ах, да, мы используем ; вместо , потому что в названиях книг могут использоваться запятые."""
                        if len(header) != 8:
                            raise ValueError("Invalid CSV format: expected 8 columns.\n"
                                             "rewrite file with this format:\n"
                                             "ISBN;Book Name;Author Name;"
                                             "Author Second Name;Author Patronymic;Publishing Year;Genre;Status")
                        # поскольку это метод add_book, мы будем читать ТОЛЬКО ОДНУ строчку файла
                        try:
                            data = [field.strip() for field in next(reader)]
                        except StopIteration:
                            raise ValueError("No books in this CSV file...")
                    if len(data) != 8:
                        raise ValueError(f"Incorrect CSV file: header has 8 columns, "
                                         f"but second string has {len(data)} columns.")
                    isbn, book_name, author_name, author_second_name, author_patronymic, year, genre, status = data
                    if not check_isbn(isbn):
                        raise ValueError("Incorrect ISBN format! "
                                         "Expected ISBN-13 with 5 parts separated with \"-\"!")
                    if self.bookshelf.get_value(isbn):
                        raise ValueError(f"Book with ISBN {isbn} already exists!")
                    book = Book(isbn)
                    book.name = book_name
                    book.author.name = author_name
                    book.author.second_name = author_second_name
                    book.author.patronymic = author_patronymic
                    try:
                        book.year = int(year)
                    except ValueError:
                        book.year = 0
                        print(f"Warning: Invalid year '{year}'. Set to 0.")
                    book.genre = genre
                    book.available = status.lower() in ("true", "yes", "1", "да")
                    self.bookshelf.insert_with_key(isbn, book)
                else:
                    raise FileExistsError(f"Expected *.csv file, got: *{fp.suffix.lower()}")
            else:
                raise FileExistsError("Expected file, not anything else!")
        else:
            raise FileExistsError("Incorrect file path!")

    @is_empty
    def delete_book(self, isbn: str):
        if not check_isbn(isbn):
            raise BookDoesntExist("Incorrect ISBN!")
        deleted_book = self.bookshelf.delete_with_key(isbn)
        if not deleted_book:
            raise BookDoesntExist("The ISBN you entered doesn't match any book")
        return deleted_book

    def give_book(self, isbn: str):
        if not check_isbn(isbn):
            raise BookDoesntExist("Incorrect ISBN!")
        book_to_give = self.find_book(isbn)
        if book_to_give.available:
            book_to_give.available = False
            return
        raise IncorrectBookStatus("unavailable")

    def receive_book(self, isbn: str):
        if not check_isbn(isbn):
            raise BookDoesntExist("Incorrect ISBN!")
        book_to_receive = self.find_book(isbn)
        if not book_to_receive.available:
            book_to_receive.available = True
            return
        raise IncorrectBookStatus("available")

    def load_from_file(self, filepath: str):
        fp = Path(filepath)
        if fp.exists():
            if fp.is_file():
                if fp.suffix.lower() == ".csv":
                    with fp.open("r", encoding="UTF-8") as book_file:
                        reader = csv.reader(book_file, delimiter=';')
                        try:
                            header = next(reader)
                        except StopIteration:
                            raise ValueError("File is empty!")
                        """мы хотим *.csv с таким заголовком:
                        ISBN;Book Name;Author Name;Author Second Name;Author Patronymic;Publishing Year;Genre;Status
                        ах, да, мы используем ; вместо , потому что в названиях книг могут использоваться запятые."""
                        if len(header) != 8:
                            raise ValueError("Invalid CSV format: expected 8 columns.\n"
                                             "rewrite file with this format:\n"
                                             "ISBN;Book Name;Author Name;"
                                             "Author Second Name;Author Patronymic;Publishing Year;Genre;Status")
                        for i, row in enumerate(reader, start=2):
                            if not row or all(cell.strip() == "" for cell in row):
                                continue
                            if len(row) != 8:
                                print(f"Warning: Line {i} skipped due to wrong number of fields: {len(row)}")
                                continue
                            data = [field.strip() for field in row]
                            isbn, book_name, author_name, author_second_name, author_patronymic, \
                                year, genre, status = data
                            if not check_isbn(isbn):
                                print(f"Warning: Line {i} skipped due to invalid ISBN: {isbn}")
                                continue
                            if self.bookshelf.get_value(isbn):
                                print(f"Warning: Line {i} skipped — book with ISBN {isbn} already exists.")
                                continue
                            book = Book(isbn)
                            book.name = book_name
                            book.author.name = author_name
                            book.author.second_name = author_second_name
                            book.author.patronymic = author_patronymic
                            try:
                                book.year = int(year)
                            except ValueError:
                                book.year = 0
                                print(f"Warning: Line {i} has invalid year '{year}'. Set to 0.")
                            book.genre = genre
                            book.available = status.lower() in ("true", "yes", "1", "да")
                            self.bookshelf.insert_with_key(isbn, book)
                else:
                    raise FileExistsError(f"Expected *.csv file, got: *{fp.suffix.lower()}")
            else:
                raise FileExistsError("Expected file, not anything else!")
        else:
            raise FileExistsError("Incorrect file path!")

    def save_to_file(self, filepath: str):
        fp = Path(filepath)
        if not fp.parent.exists():
            raise FileNotFoundError(f"Directory '{fp.parent}' does not exist.")
        if fp.suffix.lower() != ".csv":
            raise ValueError(f"Expected *.csv file, got: *{fp.suffix.lower()}")
        with fp.open("w", encoding="UTF-8", newline="") as out_file:
            writer = csv.writer(out_file, delimiter=';')
            writer.writerow([
                "ISBN", "Book Name", "Author Name", "Author Second Name",
                "Author Patronymic", "Publishing Year", "Genre", "Status"
            ])
            for book in self.bookshelf:
                writer.writerow([
                    book.isbn,
                    book.name,
                    book.author.name,
                    book.author.second_name,
                    book.author.patronymic,
                    book.year,
                    book.genre,
                    "Yes" if book.available else "No"
                ])
