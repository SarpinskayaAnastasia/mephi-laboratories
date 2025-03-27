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
    def __find_tail(self):
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
    def __pop_top(self):
        content = self.top
        self.top = self.top.next
        content.set_next(None)
        self.size -= 1
        return content

    @is_empty
    def pop_content(self, key: str):
        if self.top == key:
            return self.__pop_top()
        need_node_n1 = self.find_node_content(key)
        need_node = need_node_n1.next
        need_node_n1.set_next(need_node.next)
        need_node.set_next(None)  # обрываем связи, чтобы действительно удалить узел
        self.size -= 1
        return need_node


class SuperOnceConnected:
    def __init__(self, length: int):
        self.array = [OnceConnected() for _ in range(length)]
        try:
            self.length = int(abs(length))
        except ValueError:
            raise ValueError("Your n is bad, expected integer above 0")

    def is_n_bad(func):
        def wrapper(self, *args, **kwargs):
            n = args[0]  # дальнейшие методы необходимо писать так, чтобы первым аргументом после self был индекс!
            if not (isinstance(n, int) or n not in range(self.length)):
                raise ValueError("Your n is bad, expected integer above 0")
            return func(self, *args, **kwargs)

        return wrapper

    def __iter__(self):
        for _ in self.array:
            yield _

    def __str__(self):
        return f"[\n{'\n'.join(str(listik) for listik in self)}\n]"

    @is_n_bad
    def get_length_lnkd_lst(self, n: int) -> int:
        return len(self.array[n])

    @is_n_bad
    def adding(self, n: int, key: str, data):
        new_object = OnceNode(key, data)
        self.array[n].push_tail(new_object)

    @is_n_bad
    def removing(self, n: int, key: str):
        if len(self.array[n]) == 1:
            self.array[n] = OnceConnected()
            return None
        self.array[n].pop_content(key)


if __name__ == "__main__":
    test = OnceConnected()
    k = ''
    v = 0
    strs = gen_string(8, len(range(3, 55, 4)))
    for i in strs:
        k = i
        v = ((ord(i[0]) << 1) + 5) >> 1
        content = OnceNode(k, v)
        test.push_tail(content)
    print(test)
    print()
    print(test.find_node_content(k, searching=True))
    try:
        print(test.find_node_content('gnd5g', searching=True))
    except ValueError:
        print('HUI')
    print()
    print(test.pop_content(k))
    print(test)
    try:
        print(test.pop_content(k))
        print(test)
    except ValueError:
        print('HUI')
    print()
    frst_k = test.top.key
    print(frst_k)
    print()
    print(test.find_node_content(frst_k, searching=True))
    try:
        print(test.find_node_content('gnd5g', searching=True))
    except ValueError:
        print('HUI')
    print()
    print(test.pop_content(frst_k))
    print(test)
    try:
        print(test.pop_content(frst_k))
        print(test)
    except ValueError:
        print('HUI')
    print()
    mid_k = test.top.next.next.key
    print(mid_k)
    print()
    print(test.find_node_content(mid_k, searching=True))
    try:
        print(test.find_node_content('gnd5g', searching=True))
    except ValueError:
        print('HUI')
    print()
    print(test.pop_content(mid_k))
    print(test)
    try:
        print(test.pop_content(mid_k))
        print(test)
    except ValueError:
        print('HUI')
    print()
    print(len(test))

    print('-------------')

    super_test = SuperOnceConnected(3)
    print(super_test)
    bubu = gen_string(8, 3)
    joy = 452325
    for s in bubu:
        super_test.adding(joy % 3, s, ((joy << 2) + 8959) % 1000)
        joy += 1
    for n in test:
        super_test.adding(joy % 3, n.key, n.data)
        joy += 2
    print(super_test)
    print()
    super_test.removing(2, super_test.array[2].top.key)
    print(super_test)
    super_test.removing(1, super_test.array[1].top.next.next.key)
    print(super_test)
    super_test.removing(0, super_test.array[0].top.next.next.key)
    print(super_test)
