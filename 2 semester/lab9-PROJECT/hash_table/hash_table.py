import functools

from essentials import OnceConnected, OnceNode
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


class HashTable:
    def __init__(self, size: int):
        self.capacity = size
        self.data = [OnceConnected() for _ in range(size)]
        self.length = 0

    def __len__(self) -> int:
        return self.length

    def __str__(self):
        return f"[\n{";\n".join(str(listik) for listik in self.data)}\n]"

    def __iter__(self):
        for bucket in self.data:
            for node in bucket:
                yield node.data

    @staticmethod
    def domain_expansion(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> R:
            if self.alpha() >= 2 / 3:
                new_capacity = self.capacity + int(self.capacity * 2 / 3)
                new_hash_table = HashTable(new_capacity)
                for listik in self.data:
                    while len(listik) > 0:
                        interesting_node = listik.pop_top()
                        new_hash_table.insert_with_key(interesting_node.key, interesting_node.data)
                self.capacity = new_hash_table.capacity
                self.data = new_hash_table.data
                self.length = new_hash_table.length

            return func(self, *args, **kwargs)

        return wrapper

    def __hash_function(self, key: str) -> int:
        clean_isbn = "".join(c for c in key if c.isdigit() or c == "-")
        selected = list(map(int, clean_isbn.split("-")))
        hash_value = (selected[1] << 8) + selected[2] * 31 + selected[3] % 17 + selected[4]
        return hash_value % self.capacity

    @domain_expansion
    def insert_with_key(self, key: str, value):
        index = self.__hash_function(key)
        self.data[index].push_tail(OnceNode(key, value))
        self.length += 1

    def get_value(self, key: str):
        index = self.__hash_function(key)
        if len(self.data[index]) > 1:
            try:
                return self.data[index].find_node_content(key, True)
            except ValueError:
                return None
        predicted_node = self.data[index].top
        if predicted_node.key != key:
            return None
        return predicted_node.data

    def delete_with_key(self, key: str):
        index = self.__hash_function(key)
        if len(self.data[index]) > 1:
            try:
                self.length -= 1
                return self.data[index].pop_content(key)
            except ValueError:
                return None
        predicted_node = self.data[index].top
        if predicted_node.key != key:
            return None
        self.length -= 1
        return predicted_node.data

    def alpha(self) -> float:
        return self.length / self.capacity if self.capacity > 0 else 0


def hash_func1(isbn: str, table_size: int = 10) -> int:
    hash_value = 0
    prime = 31
    for d in isbn:
        if d.isdigit():
            hash_value = (hash_value * prime + int(d)) % table_size
    return hash_value


def hash_func2(isbn: str, table_size: int = 10) -> int:
    hash_value = 0
    prime = 31
    for d in isbn:
        if d.isdigit():
            hash_value = (hash_value * prime + int(d))
    return hash_value % table_size


def hash_func3(isbn: str, table_size: int = 10) -> int:
    """Использую эту функцию"""
    clean_isbn = "".join(c for c in isbn if c.isdigit() or c == "-")
    selected = list(map(int, clean_isbn.split("-")))
    hash_value = (selected[1] << 8) + selected[2] * 31 + selected[3] % 17 + selected[4]
    return hash_value % table_size


def hash_func4(isbn: str, table_size: int = 10) -> int:
    clean_isbn = "".join(c for c in isbn if c.isdigit() or c == "-")
    selected = list(map(int, clean_isbn.split("-")))
    return sum(selected) % table_size


def hash_func5(isbn: str, table_size: int = 10) -> int:
    prime = 0x9e3779b9
    hash_value = 0
    for ch in isbn:
        hash_value = (hash_value * prime + ord(ch)) & 0xffffffff
    hash_value ^= (hash_value >> 16)
    hash_value = (hash_value * prime) & 0xffffffff
    return hash_value % table_size


test_isbns = """978-0-14-312755-0
978-0-262-03384-8
978-0-13-110362-7
978-1-4920-5681-2
978-0-13-235088-4
978-0-596-00712-6
978-0-201-63361-0
978-1-119-45633-9
978-0-13-468599-1
978-0-596-51774-8"""


def test1():
    print('\n')
    sizes = [10, 100, 1000, 100000]
    for size in sizes:
        hashs = set()
        for isbn in test_isbns.split('\n'):
            hashs.add(hash_func1(isbn, size))
        print(f"For table with size {size} collisions={10 - len(hashs)}")
    assert True


def test2():
    print('\n')
    sizes = [10, 100, 1000, 100000]
    for size in sizes:
        hashs = set()
        for isbn in test_isbns.split('\n'):
            hashs.add(hash_func2(isbn, size))
        print(f"For table with size {size} collisions={10 - len(hashs)}")
    assert True


def test3():
    """эта показала лучшие результаты: 4 коллизии для 10 элементов в таблице и ни одной для остальных"""
    print('\n')
    sizes = [10, 100, 1000, 100000]
    for size in sizes:
        hashs = set()
        for isbn in test_isbns.split('\n'):
            hashs.add(hash_func3(isbn, size))
        print(f"For table with size {size} collisions={10 - len(hashs)}")
    assert True


def test4():
    print('\n')
    sizes = [10, 100, 1000, 100000]
    for size in sizes:
        hashs = set()
        for isbn in test_isbns.split('\n'):
            hashs.add(hash_func4(isbn, size))
        print(f"For table with size {size} collisions={10 - len(hashs)}")
    assert True


def test5():
    print('\n')
    sizes = [10, 100, 1000, 100000]
    for size in sizes:
        hashs = set()
        for isbn in test_isbns.split('\n'):
            hashs.add(hash_func5(isbn, size))
        print(f"For table with size {size} collisions={10 - len(hashs)}")
    assert True
