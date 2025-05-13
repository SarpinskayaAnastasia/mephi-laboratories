HELP = """предлагаю так:
help -> мы выводим весь перечень возможных команд

updata <название файла> -> дергаем из папки input_data данные и пишем их в нашу структуру данных

ОПЕРАЦИИ ИЗМЕНЕНИЯ СТАТУСА
give <isbn> -> мы должны установить у книги с id книги статус self.available = False
    если книга УЖЕ недоступна - говорим, что не можем ее дать
receive <isbn> -> мы должны установить у книги с id книги статус self.available = True
    если книга И ТАК доступна - пишем, что она никому не давалась

ОПЕРАЦИИ УДАЛЕНИЯ
delete <isbn> -> удаляем книжку

ОПЕРАЦИИ ДОБАВЛЕНИЯ
add <название файла> -> добавляем книжку
    если файл - говно - говорим об этом пользователю
    # прописывать в консоли ВСЕ - можно рехнуться

ОПЕРАЦИИ ПОИСКА
find <isbn> -> выводим книжку со всеми id
    если isbn некорректный - говорим об этом
    иначе - говорим, найдено ли что-то или нет
"""


def updata(filename):
    pass


def give(isbn):
    pass


def receive(isbn):
    pass


def delete(isbn):
    pass


def add(filename):
    pass


def find(isbn):
    pass


def str_to_func(konsole: str):
    parts = konsole.strip().split()
    if not parts:
        return

    command = parts[0]

    if command == "help":
        print(HELP)
        return
    elif command == "updata" and len(parts) == 2:
        updata(parts[1])
        return
    elif command == "give" and len(parts) == 2:
        give(parts[1])
        return
    elif command == "receive" and len(parts) == 2:
        receive(parts[1])
        return
    elif command == "delete" and len(parts) == 2:
        delete(parts[1])
        return
    elif command == "add" and len(parts) == 2:
        add(parts[1])
        return
    elif command == "find" and len(parts) == 2:
        find(parts[1])
        return
    else:
        print("WHAT? Type \"help\" to show all possible commands")
        return
