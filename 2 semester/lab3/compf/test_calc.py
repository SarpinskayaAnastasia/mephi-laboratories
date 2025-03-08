from pytest import approx, raises
from calc import Calc


class TestCalc:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.c = Calc()

    # Интерпретатор арифметических выражений работает только с цифрами
    def test_raises(self):
        with raises(Exception):
            self.c.compile('a')

    # Тесты на сложение
    def test_addition1(self):
        assert self.c.compile('1+2') == 3

    def test_addition2(self):
        assert self.c.compile('1+2+3+4+5+6') == 21

    def test_addition3(self):
        assert self.c.compile('(1+2)+(3+4)') == 10

    def test_addition4(self):
        assert self.c.compile('(1+(2+3)+4)') == 10

    # Тесты на вычитание
    def test_subtraction1(self):
        assert self.c.compile('1-2') == -1

    def test_subtraction2(self):
        assert self.c.compile('5-2') == 3

    def test_subtraction3(self):
        assert self.c.compile('1-2-3-4-5-6') == -19

    def test_subtraction4(self):
        assert self.c.compile('(1-2)-(3-4)') == 0

    # Тесты на умножение
    def test_multiplication1(self):
        assert self.c.compile('1*2') == 2

    def test_multiplication2(self):
        assert self.c.compile('0*3') == 0

    def test_multiplication3(self):
        assert self.c.compile('7*1*1*1') == 7

    def test_multiplication4(self):
        assert self.c.compile('2*5*2') == 20

    # Тесты на деление
    def test_division1(self):
        assert self.c.compile('1/2') == approx(0.5)

    def test_division2(self):
        assert self.c.compile('2/1') == approx(2.0)

    def test_division3(self):
        assert self.c.compile('0/3') == approx(0.0)

    def test_division4(self):
        assert self.c.compile('8/2/2/2') == approx(1.0)

    def test_division5(self):
        with raises(ZeroDivisionError):
            self.c.compile('1/0')

    # Тесты на сложные арифметические выражения
    def test_expressions1(self):
        assert self.c.compile('(1-2)') == -1

    def test_expressions2(self):
        assert self.c.compile('(1+4)*7') == 35

    def test_expressions3(self):
        assert self.c.compile('7*(8)/4') == approx(14.0)

    def test_expressions4(self):
        test = '1+2+(2*(3+7))/(5+8/3)'
        assert self.c.compile(test) == approx(eval(test))

    def test_expressions5(self):
        test = '(3-5-2*6/(1+1))/(2*5-1+4*(5*2/3))+(7+4+7/9)/(1+6/3)'
        assert self.c.compile(test) == approx(eval(test))

    # Тесты шифтинга/битового сдвига
    """
    Приоритет сдвига является низшим, поэтому часть значений с которыми сравниваю считаю ручками а не в eval
    Вычисляются значения выражений, содержащих битовые операции << и >>, 
    приоритет << является минимальным, а >> — максимальным.
    """

    def test_binary_shift_l_1(self):
        test = "8+12<<2"  # == (8+12)<<2 == 80
        assert self.c.compile(test) == approx(eval(test))

    def test_binary_shift_r_1(self):
        test = "50+8>>2"  # == 50+(8>>2) == 52
        assert self.c.compile(test) == 52

    def test_binary_shift_l_2(self):
        test = '80<<2+3'  # == 80<<(2+3) == 2560
        assert self.c.compile(test) == approx(eval(test))

    def test_binary_shift_r_2(self):
        test = '80>>2+3'  # == (80>>2)+3 == 23
        assert self.c.compile(test) == 23

    def test_binary_shift_l_3(self):
        test = "1+2+(2*(3+7))<<(5+8<<3)"  # == (1+2+(2*(3+7)))<<((5+8)<<3) == 466495420883988419750786779578368
        assert self.c.compile(test) == approx(eval(test))

    def test_binary_shift_r_3(self):
        test = "1+2+(2*(3+7))>>(5+8>>3)"  # == 1+2+((2*(3+7))>>(5+(8>>3))) == 3
        assert self.c.compile(test) == 3

    def test_binary_shift_l_4(self):
        test = '7>>8<<4'  # == (7>>8)<<4 == 0
        assert self.c.compile(test) == approx(eval(test))

    def test_binary_shift_r_4(self):
        test = '7<<8>>4'  # == 7<<(8>>4) == 7
        assert self.c.compile(test) == 7
