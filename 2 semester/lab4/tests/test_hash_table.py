import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import random
from string import ascii_letters, digits, punctuation
from hash_table import HashTable

# Параметры тестирования
NUM_ELEMENTS = 100000
KEY_LENGTH = 10
VALUE_RANGE = (1, 100000)


def gen_string(length=10, lot=1):
    for _ in range(lot):
        yield ''.join(random.choices(ascii_letters + digits + punctuation, k=length))


def gen_value(lot=1):
    cisharp = 123456542327453351
    nechto = 5451531464316
    for _ in range(lot):
        yield cisharp & nechto
        nechto = nechto >> 2 if nechto & 1 else nechto + 1


def test_hash_table():
    ht = HashTable(10)
    keys = list(gen_string(KEY_LENGTH, NUM_ELEMENTS))
    values = gen_value(NUM_ELEMENTS)

    # Тест вставки
    insert_times = []
    for key, value in zip(keys, values):
        start = time.time()
        ht.insert_with_key(key, value)
        end = time.time()
        insert_times.append(end - start)

    avg_insert_time = sum(insert_times) / NUM_ELEMENTS
    print(f"Среднее время вставки: {avg_insert_time:.6f} сек")

    # Тест поиска
    search_times = []
    for key in keys:
        start = time.time()
        ht.get_value(key)
        end = time.time()
        search_times.append(end - start)

    avg_search_time = sum(search_times) / NUM_ELEMENTS
    print(f"Среднее время поиска: {avg_search_time:.6f} сек")

    # Тест удаления
    delete_times = []
    for key in keys:
        start = time.time()
        ht.delete_with_key(key)
        end = time.time()
        delete_times.append(end - start)

    avg_delete_time = sum(delete_times) / NUM_ELEMENTS
    print(f"Среднее время удаления: {avg_delete_time:.6f} сек")


if __name__ == "__main__":
    test_hash_table()
