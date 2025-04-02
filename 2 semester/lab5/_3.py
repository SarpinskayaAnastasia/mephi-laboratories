from _2 import bin_paste_sort


class StudentsGrades:
    def __init__(self, name, subject, mark):
        self.name = name
        self.subject = subject
        self.mark = mark

    def __str__(self):
        return f"({self.name}, {self.subject}, {self.mark})\n"

    @classmethod
    def import_from_tuple(cls, data: tuple[str, str, int]):
        return cls(*data)

    '''предмет -> оценка (по убыванию) -> имя'''

    def __lt__(self, other):
        if isinstance(other, StudentsGrades):
            if self.subject == other.subject:
                if self.mark == other.mark:
                    return self.name < other.name
                return self.mark > other.mark
            return self.subject < other.subject
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, StudentsGrades):
            if self.subject == other.subject:
                if self.mark == other.mark:
                    return self.name <= other.name
                return self.mark >= other.mark
            return self.subject <= other.subject
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, StudentsGrades):
            if self.subject == other.subject:
                if self.mark == other.mark:
                    return self.name > other.name
                return self.mark < other.mark
            return self.subject > other.subject
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, StudentsGrades):
            if self.subject == other.subject:
                if self.mark == other.mark:
                    return self.name >= other.name
                return self.mark <= other.mark
            return self.subject >= other.subject
        return NotImplemented


if __name__ == "__main__":
    students = [StudentsGrades.import_from_tuple(t) for t in [("Иванов", "Математика", 85),
                                                              ("Петров", "Физика", 92),
                                                              ("Сидоров", "Математика", 78),
                                                              ("Иванов", "Физика", 90),
                                                              ("Петров", "Математика", 88),
                                                              ("Сидоров", "Информатика", 95),
                                                              ("Иванов", "Информатика", 82),
                                                              ("Петров", "Информатика", 97),
                                                              ("Сидоров", "Физика", 85)]]

    bin_paste_sort(students)
    print(*students)
