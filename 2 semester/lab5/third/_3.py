from _2 import bin_paste_sort
from essentials import HashTable

students_db = HashTable(32)  # {(subject, mark): [students]}
sub_statistics = HashTable(32)  # {subject: [sum: int, count: int, average: float]}
subjects = set()  # set[str]
grades_stats = []  # list[list[name: str, sum: int, count: int, grades: float]]


def tuple_to_str(subject: str, mark: int) -> str:
    return str(mark) + subject + str(mark)


def add_to_students_db(name: str, subject: str, mark: int):
    key = tuple_to_str(subject, mark)
    existing = students_db.get_value(key)
    if existing is not None:
        existing.append((name, subject, mark))
    else:
        students_db.insert_with_key(key, [(name, subject, mark)])


def update_sub_stats(subject: str, mark: int):
    existing = sub_statistics.get_value(subject)
    if existing is not None:
        existing[0] += mark
        existing[1] += 1
        existing[2] = existing[0] / existing[1]
    else:
        sub_statistics.insert_with_key(subject, [mark, 1, mark])


def update_grades(name: str, mark: int):
    if not grades_stats:
        grades_stats.append([name, mark, 1, mark])
    else:
        target = [name, mark, 1, mark]
        for t in grades_stats:
            if t[0] == name:
                t[1] += target[1]
                t[2] += target[2]
                t[3] = t[1] / t[2]
                return None
        grades_stats.append(target)
    bin_paste_sort(grades_stats, key=lambda x: -x[3])


def update_all_dbs(name: str, subject: str, mark: int):
    add_to_students_db(name, subject, mark)
    update_sub_stats(subject, mark)
    subjects.add(subject)
    update_grades(name, mark)

def print_top_students(grades_stats, top_n=3):
    if not grades_stats:
        print("Нет данных о студентах")
        return
    print("Лучшие студенты:")
    for i, student in enumerate(grades_stats[:top_n], 1):
        print(f"{i}. {student[0]}: {student[3]:.2f}")


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

    bin_paste_sort(TEST_DATA, key=lambda x: (x[1], -x[2], x[0]))
    print(*TEST_DATA, sep='\n')

    print()

    for args in TEST_DATA:
        update_all_dbs(*args)

    result = students_db.get_value(tuple_to_str("Математика", 85))
    print(*result, sep='\n')

    print()
    for sub in subjects:
        print(f"{sub}: {sub_statistics.get_value(sub)[2]:.2f}")

    #print()
    #print(*[(i[0], i[3]) for i in grades_stats[:3]], sep='\n')

    print()
    print_top_students(grades_stats)
