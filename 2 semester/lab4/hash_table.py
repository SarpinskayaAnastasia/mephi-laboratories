from essentials import OnceConnected, OnceNode


class HashTable:
    def __init__(self, size: int):
        self.capacity = size
        self.data = [OnceConnected() for _ in range(size)]
        self.length = 0

    def __str__(self):
        return f"[\n{";\n".join(str(listik) for listik in self.data)}\n]"

    def domain_expansion(func):
        def wrapper(self, *args, **kwargs):
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
        return sum(ord(c) for c in str(key)) % self.capacity

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
        return predicted_node

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
        return predicted_node

    def alpha(self) -> float:
        return self.length / self.capacity if self.capacity > 0 else 0
