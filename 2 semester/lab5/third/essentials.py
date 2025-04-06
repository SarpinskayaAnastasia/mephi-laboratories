class OnceNode:
    def __init__(self, key: str, data):
        self.key = key
        self.data = data
        self.next = None

    def __str__(self):
        return "{\"" + self.key + "\": " + str(self.data) + "}"

    def __eq__(self, other):
        if isinstance(other, OnceNode):
            return self.key == other.key
        elif isinstance(other, str):
            return self.key == other
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, OnceNode):
            return self.key != other.key
        elif isinstance(other, str):
            return self.key != other
        return NotImplemented

    def set_next(self, node):
        self.next = node


class OnceConnected:
    def __init__(self):
        self.top = None
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        current = self.top
        while current:  # ну поскольку наш список не циклический, мы можем себе позволить цикл `while` instead of `for`
            yield current
            current = current.next

    def __str__(self):
        if self.size:
            s = [str(node) for node in self]
            return ' -> '.join(s)
        else:
            return 'This is an empty once connected list.'

    def is_empty(func):
        def wrapper(self, *args, **kwargs):
            if not self.size:
                raise IndexError("List is empty")
            return func(self, *args, **kwargs)

        return wrapper

    @is_empty
    def __find_tail(self) -> OnceNode:
        tail = None
        for node in self:  # делаю именно так,
            # чтобы в последствии в классе циклического односвязного не
            # надо было ничего переписывать
            tail = node
        return tail

    @is_empty
    def find_node_content(self, key: str, searching=False):
        prev = None  # Для хранения предыдущего узла
        for node in self:  # Используем итератор вместо ручного обхода
            if node == key:
                return node if searching else prev
            prev = node  # Запоминаем предыдущий узел
        raise ValueError(f"Node with content {key} doesn't exist")

    def __push_top(self, node_item: OnceNode):  # push to top
        node_item.set_next(self.top)
        self.top = node_item
        self.size += 1

    def push_tail(self, node_item: OnceNode):  # push to tail
        try:
            old_tail = self.__find_tail()
            old_tail.set_next(node_item)
            self.size += 1
        except IndexError:  # если список пуст, без разницы, как добавить наш элемент
            self.__push_top(node_item)

    @is_empty
    def pop_top(self) -> OnceNode:
        content = self.top
        self.top = self.top.next
        content.set_next(None)
        self.size -= 1
        return content

    @is_empty
    def pop_content(self, key: str) -> OnceNode:
        if self.top == key:
            return self.pop_top()
        need_node_n1 = self.find_node_content(key)
        need_node = need_node_n1.next
        need_node_n1.set_next(need_node.next)
        need_node.set_next(None)  # обрываем связи, чтобы действительно удалить узел
        self.size -= 1
        return need_node


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
