from _2 import bin_paste_sort
from essentials import HashTable

students_db = HashTable(32)  # {(subject, mark): [students]}
sub_statistics = HashTable(32)  # {subject: [sum: int, num: int, average: float]}
subjects = set()


def tuple_to_str(subject: str, mark: int) -> str:
    return str(mark) + subject + str(mark)


class StudentsGrades:
    def __init__(self, name: str, subject: str, mark: int):
        self.name = name
        self.subject = subject
        self.mark = mark
        self.__add_to_students_db()
        self.__update_sub_stats()
        subjects.add(self.subject)

    def __str__(self):
        return f"({self.name}, {self.subject}, {self.mark})"

    def __add_to_students_db(self):
        key = tuple_to_str(self.subject, self.mark)
        existing = students_db.get_value(key)
        if existing is not None:
            existing.append(self)
        else:
            students_db.insert_with_key(key, [self])

    def __update_sub_stats(self):
        existing = sub_statistics.get_value(self.subject)
        if existing is not None:
            existing[0] += self.mark
            existing[1] += 1
            existing[2] = existing[0] / existing[1]
        else:
            sub_statistics.insert_with_key(self.subject, [self.mark, 1, self.mark])

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

    def __eq__(self, other):
        if isinstance(other, StudentsGrades):
            return (self.subject == other.subject) and (self.mark == other.mark) and (self.name == other.name)
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, StudentsGrades):
            return (self.subject != other.subject) or (self.mark != other.mark) or (self.name != other.name)
        return NotImplemented


if __name__ == "__main__":
    TEST_DATA = [("Иванов", "Математика", 85),
                 ("Петров", "Физика", 92),
                 ("Сидоров", "Математика", 78),
                 ("Иванов", "Физика", 90),
                 ("Петров", "Математика", 88),
                 ("Сидоров", "Информатика", 95),
                 ("Иванов", "Информатика", 82),
                 ("Петров", "Информатика", 97),
                 ("Сидоров", "Физика", 85)
                 ]
    students = [StudentsGrades.import_from_tuple(t) for t in TEST_DATA]

    bin_paste_sort(students)
    print(*students, sep='\n')

    print()

    result = students_db.get_value(tuple_to_str("Математика", 85))
    print(*result, sep='\n')

    print()
    for sub in subjects:
        print(f"{sub}: {sub_statistics.get_value(sub)[2]:.2f}")
