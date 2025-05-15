def check_isbn(isbn: str) -> bool:
    isbn = isbn.strip()
    if isbn.upper().startswith("ISBN"):
        isbn = isbn[4:].lstrip()

    parts = isbn.split("-")
    if len(parts) != 5 or not all(part.isdigit() for part in parts):
        return False

    digits_str = ''.join(parts)
    if len(digits_str) != 13:
        return False

    digits = list(map(int, digits_str[:12]))
    check_digit = int(digits_str[12])
    s = sum(d * (3 if i % 2 else 1) for i, d in enumerate(digits))
    return check_digit == (10 - s % 10) % 10


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


def test_isbn_only_digits():
    assert check_isbn("9782266111560") is False


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


def test_isbn_double_dash():
    assert check_isbn("978-2--26611156-0") is False


def test_all():
    test_isbns = """978-0-14-312755-0
978-0-262-03384-8
978-0-13-110362-7
978-1-4920-5681-2
978-0-13-235088-4
978-0-596-00712-6
978-0-201-63361-0
978-1-119-45633-9
978-0-13-468599-1
978-0-596-51774-8""".split('\n')
    for isbn in test_isbns:
        assert check_isbn(isbn) is True
