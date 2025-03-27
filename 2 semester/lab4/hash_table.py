import time
from essentials import *


class HashTable:
    def __init__(self, size: int):
        self.capacity = size
        self.data = SuperOnceConnected(size)
        self.length = 0

    def domain_expansion(func):
        def wrapper(self, *args, **kwargs):
            if self.alpha() >= 2 / 3:
                extending = int(self.capacity * 2 / 3)
                self.capacity += extending
                self.data.extend([[] for _ in range(extending)])  # ТАК НЕ ПОЙДЕТ ЭТО ГОВНО РЕШЕНИЕ
            return func(self, *args, **kwargs)

        return wrapper

    def __hash_function(self, key: str) -> int:
        return sum(ord(c) for c in str(key)) % self.capacity

    @domain_expansion
    def insert_with_key(self, key: str, value):
        pass

    def get_value(self, key: str):
        pass

    def delete_with_key(self, key: str):
        pass

    def alpha(self) -> float:
        return self.length / self.capacity if self.capacity > 0 else 0


if __name__ == "__main__":
    h = HashTable(1000)
