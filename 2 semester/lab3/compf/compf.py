#!/usr/bin/env python3

# Смотреть строки: 37, 53, 72, 107

import re
from stack import Stack


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
        # Последовательный вызов для всех символов
        # взятой в скобки формулы метода process_symbol

        # Тут начинаются мои необратимые изменения, которые я
        # закомментировал сильнее, чем сам код

        # Уродую строку, чтоб она была сначала в скобках.
        # Это необходимо типо, чтоб эта херота определяла
        # нормально порядок действий.
        str_in = f"({str_in})"

        # Тут я заменяю все знаки операций и скобок на формат ~*операция*~
        # Это нужно, чтоб потом сплитнуть по тильдам,
        # что и делаю в последней сторке чанка
        for op in list("+-*/()") + ["<<", ">>"]:
            str_in = str_in.replace(op, f"~{op}~")
        list_in = str_in.split("~")

        # Удаляю мусорные элементы массива после сплита. Они
        # образуются из-за сплита по тильдам. У нас появляются две ''
        # по краям массива.
        del list_in[0]
        del list_in[-1]

        # Тут, по сути, я просто повторяю то, что было в самом
        # алгоритме. Всё работает, это победа.
        for seq in list_in:
            self.process_sequence(seq)
        return " ".join(self.data)

    # Обработка уже не символа, а последовательности символов. Окак
    # Тут я изменял эту херота, чтоб она понимала операции "<<" и
    # ">>"
    def process_sequence(self, seq):
        if seq == "(":
            self.s.push(seq)
        elif seq == ")":
            self.process_suspended_operators(seq)
            self.s.pop()
        elif seq in list("+-*/") + ["<<", ">>"]:
            self.process_suspended_operators(seq)
            self.s.push(seq)
        else:
            self.check_symbol(seq)
            self.process_value(seq)

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

    # Определение приоритета операции
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
        str_in = input("Арифметическая  формула: ")
        print(f"Результат её компиляции: {c.compile(str_in)}")
        print()
