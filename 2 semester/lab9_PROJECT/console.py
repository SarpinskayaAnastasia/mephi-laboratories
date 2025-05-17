from data_struct import Library

HELP = """предлагаю так:
help -> мы выводим весь перечень возможных команд

updata [название файла] -> дергаем из папки input_data данные и пишем их в нашу структуру данных

ОПЕРАЦИИ ИЗМЕНЕНИЯ СТАТУСА
give [isbn] -> мы должны установить у книги с id книги статус self.available = False
    если книга УЖЕ недоступна - говорим, что не можем ее дать
receive [isbn] -> мы должны установить у книги с id книги статус self.available = True
    если книга И ТАК доступна - пишем, что она никому не давалась

ОПЕРАЦИИ УДАЛЕНИЯ
delete [isbn] -> удаляем книжку

ОПЕРАЦИИ ДОБАВЛЕНИЯ
add [название файла] -> добавляем книжку
    если файл - говно - говорим об этом пользователю
    # прописывать в консоли ВСЕ - можно рехнуться

ОПЕРАЦИИ ПОИСКА
find [isbn] -> выводим книжку
    если isbn некорректный - говорим об этом
    иначе - говорим, найдено ли что-то или нет
"""


def updata(filename: str, library: Library):
    try:
        library.load_from_file(filename)
        print(f"Data loaded successfully from {filename}.")
    except Exception as e:
        print(f"Error: {e}")


def give(isbn: str, library: Library):
    try:
        library.give_book(isbn)
        print(f"Book with ISBN {isbn} is now marked as unavailable.")
    except Exception as e:
        print(f"Error: {e}")


def receive(isbn: str, library: Library):
    try:
        library.receive_book(isbn)
        print(f"Book with ISBN {isbn} is now marked as available.")
    except Exception as e:
        print(f"Error: {e}")


def delete(isbn: str, library: Library):
    try:
        library.delete_book(isbn)
        print(f"Book with ISBN {isbn} has been deleted.")
    except Exception as e:
        print(f"Error: {e}")


def add(filename: str, library: Library):
    try:
        library.add_book(filename)
        print(f"Book from {filename} has been added.")
    except Exception as e:
        print(f"Error: {e}")


def find(isbn: str, library: Library):
    try:
        book = library.find_book(isbn)
        if book:
            print(f"Book found: {book.name} by {book.author.name}, ISBN: {book.isbn}")
        else:
            print("Book not found.")
    except Exception as e:
        print(f"Error: {e}")


def str_to_func(konsole: str, library: Library):
    parts = konsole.strip().split()
    if not parts:
        return

    command = parts[0]

    if command == "help":
        print(HELP)
        return
    elif command == "updata" and len(parts) == 2:
        updata(parts[1], library)
        return
    elif command == "give" and len(parts) == 2:
        give(parts[1], library)
        return
    elif command == "receive" and len(parts) == 2:
        receive(parts[1], library)
        return
    elif command == "delete" and len(parts) == 2:
        delete(parts[1], library)
        return
    elif command == "add" and len(parts) == 2:
        add(parts[1], library)
        return
    elif command == "find" and len(parts) == 2:
        find(parts[1], library)
        return
    else:
        print("WHAT? Type [help] to show all possible commands")
        return
