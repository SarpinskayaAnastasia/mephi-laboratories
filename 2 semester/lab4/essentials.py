import random
from string import ascii_letters, digits, punctuation


def gen_string(length=10, lot=1) -> str:
    for _ in range(lot):
        yield ''.join(random.choices(ascii_letters + digits + punctuation, k=length))


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
