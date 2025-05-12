class Author:
    def __init__(self):
        self.name = ""
        self.second_name = ""
        self.patronymic = ""


class Book:
    def __init__(self):
        self.id = 0
        self.isbn = ""
        self.name = ""
        self.author = ""
        self.year = 0
        self.genre = 0
        self.available = True
