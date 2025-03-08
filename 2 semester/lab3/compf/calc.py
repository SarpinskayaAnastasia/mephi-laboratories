#!/usr/bin/env python3

import re
from operator import add, sub, mul, truediv, rshift, lshift
from stack import Stack
from compf import Compf


class Calc(Compf):
    """
    Интерпретатор арифметических выражений вычисляет значения
    правильных арифметических формул, в которых в качестве
    операндов допустимы только цифры [0-9]
    """

    SYMBOLS = re.compile("[0-9]")

    def __init__(self):
        # Инициализация (конструктор) класса Compf
        super().__init__()
        # Создание стека чисел для работы стекового калькулятора
        self.r = Stack()

    # Интерпретация арифметического выражения
    def compile(self, string):
        Compf.compile(self, string)
        return self.r.top()

    # Обработка цифры
    def process_value(self, c):
        self.r.push(int(c))

    # Обработка символа операции
    # lshift - битовый сдвиг влево; rshift - битовый сдвиг вправо
    def process_oper(self, c):
        second, first = self.r.pop(), self.r.pop()
        self.r.push({"+": add, "-": sub, "*": mul, "/": truediv, "<<": lshift, ">>": rshift}[c](first, second))


if __name__ == "__main__":
    c = Calc()
    while True:
        equation = input("Арифметическое выражение: ")
        print(f"Результат его вычисления: {c.compile(equation)}")
        print()
