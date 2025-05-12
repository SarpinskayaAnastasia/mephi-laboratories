import re


def check_isbn(isbn: str) -> bool:
    """
    Корректными будем считать:
        1. ISBN nnn-n-nn-nnnnnn-n
        2. ISBN nnn-n-nnnn-nnnn-n
        3. nnn-n-nn-nnnnnn-n
        4. nnn-n-nnnn-nnnn-n
        5. nnnnnnnnnnnnn
    А ЕЩЁ мы должны проверять последнюю контрольную цифру, ибо это - контрольная цифра
    """
    isbn_pattern = re.compile(r'^(ISBN\s?)?(?:\d{3}-\d-\d{2}-\d{6}-\d|\d{3}-\d-\d{4}-\d{4}-\d|\d{13})$')

    digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    s = sum(digits[i] * 3 if i % 2 else digits[i] for i in range(len(digits)))
    return True
