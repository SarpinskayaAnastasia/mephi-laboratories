#!/usr/bin/env python3

# Смотреть строки: 37, 53, 72, 107

import re
from stack import Stack


def clear_empty_strs(array: list[str]):
    while '' in array:
        array.remove('')


class Compf:
    """
    Стековый компилятор формул преобразует правильные
    арифметические формулы (цепочки языка, задаваемого
    грамматикой G0) в программы для стекового калькулятора
    (цепочки языка, определяемого грамматикой Gs):

    G0:
        F  ->  T  |  F+T  |  F-T
        T  ->  M  |  T*M  |  T/M
        M  -> (F) |   V
        V  ->  a  |   b   |   c   |  ...  |    z

    Gs:
        e  ->  e e + | e e - | e e * | e e / |
                     | a | b | ... | z
    В качестве операндов в формулах допустимы только
    однобуквенные имена переменных [a-zA-Z]+
    """

    SYMBOLS = re.compile("[a-zA-Z]+")

    def __init__(self):
        # Создание стека отложенных операций
        self.s = Stack()
        # Создание списка с результатом компиляции
        self.data = []

    def compile(self, str_in):
        self.data.clear()
        str_in = f"({str_in})"

        for oper in list("+-*/()") + ["<<", ">>"]:
            str_in = str_in.replace(oper, f"_{oper}_")
        list_in = str_in.split("_")

        clear_empty_strs(list_in)

        for c in list_in:
            self.process_sequence(c)
        return " ".join(self.data)

    def process_sequence(self, c):
        if c == "(":
            self.s.push(c)
        elif c == ")":
            self.process_suspended_operators(c)
            self.s.pop()
        elif c in list("+-*/") + ["<<", ">>"]:
            self.process_suspended_operators(c)
            self.s.push(c)
        else:
            self.check_symbol(c)
            self.process_value(c)

    # Обработка отложенных операций
    def process_suspended_operators(self, c):
        while self.is_precedes(self.s.top(), c):
            self.process_oper(self.s.pop())

    # Обработка имени переменной
    def process_value(self, c):
        self.data.append(c)

    # Обработка символа операции
    def process_oper(self, c):
        self.data.append(c)

    # Проверка допустимости символа
    @classmethod
    def check_symbol(self, c):
        if not self.SYMBOLS.match(c):
            raise Exception(f"Недопустимый символ '{c}'")

    # Определение приоритета операции.
    # Вычисляются значения выражений, содержащих битовые операции << и >>, приоритет которых считается равным
    # приоритету сложения и вычитания.
    @staticmethod
    def priority(c):
        return 1 if (c == "+" or c == "-" or c == "<<" or c == ">>") else 2

    # Определение отношения предшествования
    @staticmethod
    def is_precedes(a, b):
        if a == "(":
            return False
        elif b == ")":
            return True
        else:
            return Compf.priority(a) >= Compf.priority(b)


if __name__ == "__main__":
    c = Compf()
    while True:
        equation = input("Арифметическая  формула: ")
        print(f"Результат её компиляции: {c.compile(equation)}")
        print()
