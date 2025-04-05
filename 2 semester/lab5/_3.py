from _2 import bin_paste_sort


class StudentsGrades:
    _students = []        # все студенты
    _grades_db = {}       # {name: [grades]}
    _students_db = {}     # {(subject, mark): [students]}
    _subjects_stats = {}  # {subject: {'total_marks': sum, 'student_count': num}}

    def __init__(self, name, subject, mark):
        self.name = name
        self.subject = subject
        self.mark = mark
        self._add_to_db()
        self._update_subject_stats()
        self._add_student()

    def __str__(self):
        return f"({self.name}, {self.subject}, {self.mark})\n"
    
    def __repr__(self):
        return f"Student({self.name}, {self.subject}, {self.mark})"
    
    def _add_student(self):
        self._students.append(self)
        if self.name not in self._grades_db:
            self._grades_db[self.name] = []
        self._grades_db[self.name].append(self.mark)

    def _update_subject_stats(self):
        if self.subject not in StudentsGrades._subjects_stats:
            StudentsGrades._subjects_stats[self.subject] = {
                'total_marks': 0,
                'student_count': 0
            }
        StudentsGrades._subjects_stats[self.subject]['total_marks'] += self.mark
        StudentsGrades._subjects_stats[self.subject]['student_count'] += 1

    def _add_to_db(self):
        key = (self.subject, self.mark)
        if key not in StudentsGrades._students_db:
            StudentsGrades._students_db[key] = []
        StudentsGrades._students_db[key].append(self)

    @classmethod
    def get_average_grades(cls):
        averages = {}
        for subject, stats in cls._subjects_stats.items():
            total = stats['total_marks']
            count = stats['student_count']
            averages[subject] = total / count if count != 0 else 0
        return averages
    
    @classmethod
    def calculate_average_grades(cls):
        averages = cls.get_average_grades()
        print("Средние оценки по предметам:")
        for subject, avg in averages.items():
            print(f"{subject}: {avg:.2f}")

    @classmethod
    def search_by_grade_and_subject(cls, subject, mark):
        students = cls._students_db.get((subject, mark), [])
        if not students:
            return f"Студенты с оценкой {mark} по предмету {subject} не найдены."
        result = "\n".join([f"('{s.name}', '{s.subject}', {s.mark})" for s in students])
        return f"Студенты с оценкой {mark} по предмету {subject}:\n{result}"
    
    @classmethod
    def _calculate_averages(cls):
        """вычисляем средний балл для каждого студента"""
        averages = {}
        for name, grades in cls._grades_db.items():
            total = 0
            count = 0
            for grade in grades:
                total += grade
                count += 1
            averages[name] = total / count if count != 0 else 0
        return averages
    
    @classmethod
    def selection_sort_students_max(cls, averages, n):
        sorted_students = []
        names = list(averages.keys())
        
        for i in range(min(n, len(names))):
            max_idx = i
            for j in range(i+1, len(names)):
                if averages[names[j]] > averages[names[max_idx]]:
                    max_idx = j
            names[i], names[max_idx] = names[max_idx], names[i]
            sorted_students.append((names[i], averages[names[i]]))
        return sorted_students

    @classmethod
    def get_top_students(cls, n=3):
        """возвращает топ-n студентов с наивысшим средним баллом"""
        averages = cls._calculate_averages()
        sorted_students = cls.selection_sort_students_max(averages, n)
        return sorted_students[:n]
    
    @classmethod
    def print_top_students(cls, n=3):
        top_students = cls.get_top_students(n)
        print("Лучшие студенты:")
        for i, (name, avg) in enumerate(top_students, 1):
            print(f"{i}. {name}: {avg:.2f}")

    @classmethod
    def import_from_tuple(cls, data: tuple[str, str, int]):
        return cls(*data)

## почему не так:
    # def __lt__(self, other):
    #     if not isinstance(other, StudentsGrades):
    #         return NotImplemented
    #     return (self.subject, -self.mark, self.name) < (other.subject, -other.mark, other.name)

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
    TEST_DATA = [("Иванов", "Математика", 85),
                 ("Петров", "Физика", 92),
                 ("Сидоров", "Математика", 78),
                 ("Иванов", "Физика", 90),
                 ("Петров", "Математика", 88),
                 ("Сидоров", "Информатика", 95),
                 ("Иванов", "Информатика", 82),
                 ("Петров", "Информатика", 97),
                 ("Сидоров", "Физика", 85)]
    students = [StudentsGrades.import_from_tuple(t) for t in TEST_DATA]

    bin_paste_sort(students)
    print(*students)

    print(StudentsGrades.search_by_grade_and_subject("Математика", 85))
    
    print()
    StudentsGrades.calculate_average_grades()

    print()
    StudentsGrades.print_top_students(3)
