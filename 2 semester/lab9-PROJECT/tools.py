import re


def check_isbn(isbn: str) -> bool:
    """
    Корректными будем считать:
        1. ISBN nnn-n-nn-nnnnnn-n
        2. ISBN nnn-n-nnnn-nnnn-n
        3. ISBN nnn-n-nnn-nnnnn-n
        4. nnn-n-nn-nnnnnn-n
        5. nnn-n-nnnn-nnnn-n
        6. nnn-n-nnn-nnnnn-n
        7. nnnnnnnnnnnnn
    А ЕЩЁ мы должны проверять последнюю контрольную цифру, ибо это - контрольная цифра
    """
    isbn_pattern = re.compile(
        r'^(ISBN\s?)?(?:\d{3}-\d-\d{2}-\d{6}-\d|\d{3}-\d-\d{3}-\d{5}-\d|\d{3}-\d-\d{4}-\d{4}-\d|\d{13})$')
    if isbn_pattern.match(isbn):
        isbn = isbn.lstrip("ISBN ")
        isbn = isbn.replace("-", "")
        digits = list(int(isbn[i]) for i in range(12))
        s = sum(digits[i] * 3 if i % 2 else digits[i] for i in range(len(digits)))
        return int(isbn[-1]) == (10 - s % 10) % 10
    return False


# Корректные форматы
def test_isbn_correct_format1():
    assert check_isbn("ISBN 978-2-26-611156-0") is True


def test_isbn_correct_format2():
    assert check_isbn("978-2-2661-1156-0") is True


def test_isbn_correct_format3():
    assert check_isbn("ISBN 978-2-266-11156-0") is True


def test_isbn_correct_format4():
    assert check_isbn("978-2-26-611156-0") is True


def test_isbn_correct_format5():
    assert check_isbn("ISBN 978-2-2661-1156-0") is True


def test_isbn_correct_format6():
    assert check_isbn("978-2-266-11156-0") is True


def test_isbn_correct_format7():
    assert check_isbn("9782266111560") is True


# Некорректные ISBN
def test_isbn_wrong_check_digit():
    assert check_isbn("ISBN 978-2-266-11156-X") is False


def test_isbn_too_short():
    assert check_isbn("978-2-266-11156") is False


def test_isbn_missing_digit_with_prefix():
    assert check_isbn("ISBN 978-2-266-11156") is False


def test_isbn_too_long():
    assert check_isbn("978-2-266-11156-01") is False


def test_isbn_invalid_chars():
    assert check_isbn("978-2-266-11156-XYZ") is False


def test_isbn_extra_dash():
    assert check_isbn("978-2-266-11156-0-") is False


def test_isbn_wrong_format_still_fails():
    assert check_isbn("ISBN 978-2-266-1115-6-1") is False


def test_isbn_wrong_check_digit_no_dashes():
    assert check_isbn("97812345678X0") is False
