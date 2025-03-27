class OnceNode:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)

    def set_next(self, node):
        self.next = node

    def __eq__(self, other):
        if isinstance(other, OnceNode):
            return self.data == other.data
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, OnceNode):
            return self.data != other.data
        return NotImplemented


class DoubleNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def __str__(self):
        return str(self.data)

    def __eq__(self, other):
        if isinstance(other, DoubleNode):
            return self.data == other.data
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, DoubleNode):
            return self.data != other.data
        return NotImplemented

    def set_next_prev(self, node_n, node_p):
        self.next = node_n
        self.prev = node_p

    def set_next(self, node):
        self.next = node

    def set_prev(self, node):
        self.prev = node


class OnceConnected:
    def __init__(self):
        self.top = None
        self.size = 0

    def __str__(self):
        if self.size:
            s = []
            obj = self.top
            for _ in range(self.size):
                s.append(str(obj))
                obj = obj.next
            return ' -> '.join(s)
        else:
            return 'This is an empty once connected list.'

    def is_n_correct(self, n: int):
        if n not in range(self.size):
            raise IndexError(f"Incorrect index, expected integer number from 0 to {self.size - 1}")

    def is_empty(self):
        if not self.size:
            raise IndexError("List is empty")

    def find_tail(self):
        self.is_empty()
        tail = self.top
        for _ in range(self.size - 1):  # делаю именно так,
            # чтобы в последствии в классе циклического односвязного не
            # надо было ничего переписывать
            tail = tail.next
        return tail

    # Что мы тут делаем? В общем, тут как бы два режима: поиск для пуша и поиск просто. В случае пуша нам удобнее
    # использовать предыдущий от искомого узел. А в случае поиска нам нужен именно тот, который ищем)
    def find_n_node(self, index: int, searching=False):
        self.is_empty()
        self.is_n_correct(index)
        if searching and not index:
            return self.top
        prev = self.top
        res = self.top.next
        while index != 1:
            prev = prev.next
            res = res.next
            index -= 1
        if searching:
            return res
        return prev

    # Тут все то же самое
    def find_node_content(self, node_content: OnceNode, searching=False):
        self.is_empty()
        if searching and self.top == node_content:
            return self.top
        elif self.size != 1 and self.top != node_content:
            prev = self.top
            res = self.top.next
            for _ in range(self.size - 1):
                if res == node_content:
                    return res if searching else prev
                res = res.next
                prev = prev.next
        raise ValueError(f"Node with content {node_content} doesn't exist")

    def push_top(self, node_item: OnceNode):  # push to top
        node_item.set_next(self.top)
        self.top = node_item
        self.size += 1

    def push_tail(self, node_item: OnceNode):  # push to tail
        try:
            old_tail = self.find_tail()
            old_tail.set_next(node_item)
            self.size += 1
        except IndexError:  # если список пуст, без разницы, как добавить наш элемент
            self.push_top(node_item)

    def push_n(self, index, node_item: OnceNode):
        if index == self.size:
            self.push_tail(node_item)
            return None
        self.is_n_correct(index)
        if not index:
            self.push_top(node_item)
            return None
        try:
            n_1 = self.find_n_node(index)
            old_n = n_1.next
            n_1.set_next(node_item)
            node_item.set_next(old_n)
            self.size += 1
        except IndexError:
            self.push_top(node_item)  # то же самое

    def pop_top(self):
        self.is_empty()
        content = self.top
        self.top = self.top.next
        content.set_next(None)
        self.size -= 1
        return content

    def pop_tail(self):
        self.is_empty()
        if self.size == 1:
            return self.pop_top()
        new_tail = self.find_n_node(self.size - 1)  # мы не ищем сам хвост, а предыдущий от него элемент
        content = new_tail.next
        new_tail.set_next(None)
        self.size -= 1
        return content

    def pop_content(self, node_content: OnceNode):
        self.is_empty()
        if self.top == node_content:
            return self.pop_top()
        need_node_n1 = self.find_node_content(node_content)
        need_node = need_node_n1.next
        need_node_n1.set_next(need_node.next)
        need_node.set_next(None)  # обрываем связи, чтобы действительно удалить узел
        self.size -= 1
        return need_node

    def pop_n(self, index):
        self.is_empty()
        self.is_n_correct(index)
        need_node_n1 = self.find_n_node(index)
        need_node = need_node_n1.next
        need_node_n1.set_next(need_node.next)
        need_node.set_next(None)
        self.size -= 1
        return need_node


class DoubleConnected(OnceConnected):
    def __init__(self):
        super().__init__()
        self.tail = None

    def __str__(self):
        if self.size:
            s = []
            obj = self.top
            for _ in range(self.size):
                s.append(str(obj))
                obj = obj.next
            return ' <-> '.join(s)
        else:
            return 'This is an empty doubly connected list.'

    def find_tail(self):
        return self.tail  # не будем использовать эту функцию, но на случай вызова лучше, чтобы она была быстрой

    def find_n_node(self, index: int, searching=False) -> DoubleNode:  # теперь режим поиска - атавизм)
        self.is_empty()
        self.is_n_correct(index)
        res = self.top
        while index != 0:
            res = res.next
            index -= 1
        return res

    def find_node_content(self, node_content: DoubleNode, searching=False):
        self.is_empty()
        if self.top == node_content:
            return self.top
        elif self.tail == node_content:
            return self.tail
        elif self.size != 1:
            res = self.top.next
            for _ in range(self.size):
                if res == node_content:
                    return res
                res = res.next
        raise ValueError(f"Node with content {node_content} doesn't exist")

    def push_top(self, node_item: DoubleNode):
        if self.size:
            node_item.set_next(self.top)
            self.top.set_prev(node_item)
            self.top = node_item
        else:
            self.top = self.tail = node_item
        self.size += 1

    def push_tail(self, node_item: DoubleNode):
        if self.size:
            node_item.set_prev(self.tail)
            self.tail.set_next(node_item)
            self.tail = node_item
        else:
            self.top = self.tail = node_item
        self.size += 1

    def push_n(self, index, node_item: DoubleNode):
        self.is_n_correct(index)
        if not index:
            self.push_top(node_item)
            return None
        elif index == self.size - 1:
            self.push_tail(node_item)
            return None
        try:
            old_n = self.find_n_node(index)
            pr = old_n.prev
            node_item.set_next_prev(old_n, pr)
            pr.set_next(node_item)
            old_n.set_prev(node_item)
            self.size += 1
        except IndexError:
            self.push_top(node_item)

    def pop_top(self):
        self.is_empty()
        content = self.top
        self.top = self.top.next
        if self.top:
            self.top.prev = None
        else:
            self.tail = None
        content.set_next_prev(None, None)
        self.size -= 1
        return content

    def pop_tail(self):
        self.is_empty()
        content = self.tail
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.top = None
        content.set_next_prev(None, None)
        self.size -= 1
        return content

    def pop_content(self, node_content: DoubleNode):
        self.is_empty()
        if self.top == node_content:
            return self.pop_top()
        elif self.tail == node_content:
            return self.pop_tail()
        need_node = self.find_node_content(node_content)
        pr = need_node.prev
        nx = need_node.next
        pr.set_next(nx)
        nx.set_prev(pr)
        need_node.set_next_prev(None, None)
        self.size -= 1
        return need_node

    def pop_n(self, index):
        self.is_empty()
        self.is_n_correct(index)
        if not index:
            return self.pop_top()
        elif index == self.size - 1:
            return self.pop_tail()
        need_node = self.find_n_node(index)
        pr = need_node.prev
        nx = need_node.next
        pr.set_next(nx)
        nx.set_prev(pr)
        need_node.set_next_prev(None, None)
        self.size -= 1
        return need_node


class CycleOnceConnected(OnceConnected):
    def __str__(self):
        return '-> ' + super().__str__() + ' ->' if self.size else super().__str__() + ' (Circular!)'

    def find_n_node(self, index: int, searching=False) -> OnceNode:
        self.is_empty()
        self.is_n_correct(index)
        if not index:
            return self.top if searching else self.find_tail()
        prev = self.top
        res = self.top.next
        while index != 1:
            prev = prev.next
            res = res.next
            index -= 1
        if searching:
            return res
        return prev

    def find_node_content(self, node_content: OnceNode, searching=False):
        self.is_empty()
        if self.top == node_content:
            return self.top if searching else self.find_tail()
        elif self.size != 1:
            prev = self.top
            res = self.top.next
            for _ in range(self.size):
                if res == node_content:
                    return res if searching else prev
                res = res.next
                prev = prev.next
        raise ValueError(f"Node with content {node_content} doesn't exist")

    def make_cycle(self):
        self.is_empty()
        tail = self.find_tail()
        if not tail.next:
            tail.set_next(self.top)

    def push_top(self, node_item: OnceNode):
        if not self.size:
            self.top = node_item
            self.size += 1
            self.make_cycle()
        else:
            node_item.set_next(self.top)
            tail = self.find_tail()
            tail.set_next(node_item)
            self.top = node_item
            self.size += 1

    def push_tail(self, node_item: OnceNode):
        if not self.size:
            self.push_top(node_item)
        else:
            tail = self.find_tail()
            tail.set_next(node_item)
            node_item.set_next(self.top)
            self.size += 1

    def drop(self):
        if self.size == 1:
            content = self.top
            self.top = None
            self.size = 0
            return content

    def pop_top(self):
        self.is_empty()
        c = self.drop()
        if c:
            return c
        content = self.top
        self.top = self.top.next
        tail = self.find_tail()
        tail.set_next(self.top)
        content.set_next(None)
        self.size -= 1
        return content

    def pop_tail(self):
        self.is_empty()
        c = self.drop()
        if c:
            return c
        new_tail = self.find_n_node(self.size - 1)
        content = self.find_tail()
        new_tail.set_next(self.top)
        content.set_next(None)
        self.size -= 1
        return content

    def pop_content(self, node_content: OnceNode):
        self.is_empty()
        pr = self.find_node_content(node_content)
        need_node = pr.next
        c = self.drop()  # эта часть кода выполняется,
        # если мы нашли-таки нужный узел, а значит нужный узел
        # располагался "в начале/конце"
        if c:
            return c
        nx = need_node.next
        pr.set_next(nx)
        need_node.set_next(None)
        self.size -= 1
        return need_node

    def pop_n(self, index):
        self.is_empty()
        self.is_n_correct(index)
        pr = self.find_n_node(index)
        need_node = pr.next
        c = self.drop()  # эта часть кода выполняется, если мы нашли-таки нужный узел, а значит нужный узел
        # располагался "в начале/конце"
        if c:
            return c
        nx = need_node.next
        pr.set_next(nx)
        need_node.set_next(None)
        self.size -= 1
        return need_node


class CycleDoubleConnected(DoubleConnected):
    def __str__(self):
        return '<-> ' + super().__str__() + ' <->' if self.size else super().__str__() + ' (Circular!)'

    def make_cycle(self):
        self.is_empty()
        if not (self.top.prev and self.tail.next):
            self.top.set_prev(self.tail)
            self.tail.set_next(self.top)

    def push_top(self, node_item: DoubleNode):
        if not self.size:
            self.top = self.tail = node_item
            self.size += 1
            self.make_cycle()
        else:
            node_item.set_next_prev(self.top, self.tail)
            self.top.set_prev(node_item)
            self.tail.set_next(self.tail.prev)
            self.top = node_item
            self.size += 1

    def push_tail(self, node_item: DoubleNode):  # в циклическом списке этот вид пуша одинаков
        self.push_top(node_item)

    def push_n(self, index: int, node_item: DoubleNode):
        self.is_n_correct(index)
        if not index:
            self.push_top(node_item)
            return None
        elif index == self.size - 1:
            self.push_tail(node_item)
            return None
        try:
            old_n = self.find_n_node(index)
            pr = old_n.prev
            node_item.set_next_prev(old_n, pr)
            pr.set_next(node_item)
            old_n.set_prev(node_item)
            self.size += 1
        except IndexError:
            self.push_top(node_item)

    def drop(self):
        if self.size == 1:
            content = self.top
            self.top = self.tail = None
            self.size = 0
            return content

    def pop_top(self):
        self.is_empty()
        content = self.top
        c = self.drop()
        if c:
            return c
        self.top = self.top.next
        self.tail.set_next(self.top)
        self.top.set_prev(self.tail)
        content.set_next_prev(None, None)
        self.size -= 1
        return content

    def pop_tail(self):
        self.is_empty()
        content = self.tail
        c = self.drop()
        if c:
            return c
        self.tail = self.tail.prev
        self.tail.set_next(self.top)
        self.top.set_prev(self.tail)
        content.set_next_prev(None, None)
        self.size -= 1
        return content

    def pop_content(self, node_content: DoubleNode):
        self.is_empty()
        if self.top == node_content:
            return self.pop_top()
        elif self.tail == node_content:
            return self.pop_tail()
        need_node = self.find_node_content(node_content)
        c = self.drop()  # эта часть кода выполняется, если мы нашли-таки нужный узел, а значит нужный узел
        # располагался "в начале/конце"
        if c:
            return c
        pr = need_node.prev
        nx = need_node.next
        pr.next = nx
        nx.prev = pr
        need_node.set_next_prev(None, None)
        self.size -= 1
        return need_node

    def pop_n(self, index):
        self.is_empty()
        self.is_n_correct(index)
        need_node = self.find_n_node(index)
        c = self.drop()  # эта часть кода выполняется, если мы нашли-таки нужный узел, а значит нужный узел
        # располагался "в начале/конце"
        if c:
            return c
        pr = need_node.prev
        nx = need_node.next
        pr.set_next(nx)
        nx.set_prev(pr)
        need_node.set_next_prev(None, None)
        self.size -= 1
        return need_node


if __name__ == "__main__":
    p = OnceConnected()
    print(p)
    for i in range(1, 20, 4):
        p.push_tail(OnceNode(i))
    print(p)
    p.push_top(OnceNode(77))
    print(p)
    p.push_n(4, OnceNode(5))
    print(p)
    print()
    print("removing top")
    print(p.pop_top())
    print(p)
    print("removing tail")
    print(p.pop_tail())
    print(p)
    print(p.pop_content(OnceNode(13)))
    print("removing 13")
    print(p)
    print("removing el with index 2")
    print(p.pop_n(2))
    print(p)
    print()

    t = DoubleConnected()
    print(t)
    for i in range(1, 20, 3):
        t.push_top(DoubleNode(i)) if i % 2 else t.push_tail(DoubleNode(i))
    print(t)
    print(t.find_node_content(DoubleNode(7)), 'found!')
    print(t.pop_content(DoubleNode(7)), 'removed!')
    print(t)
    print(t.find_n_node(3), 'found!')
    print(t.pop_n(3), 'removed!')
    print(t)

    print()
    c1 = CycleOnceConnected()
    print(c1)
    c1.push_top(OnceNode(1))
    print(c1)

    try:
        c1.push_n(10, OnceNode(55))
        print("add 55 at index 10")
        print(c1)
    except IndexError:
        print(f'А вот не получится запушить элемент на 11 позицию, когда в списке {c1.size} элементов')
    c1.push_n(1, OnceNode(100))
    print("add 100 at index 1")
    print(c1)

    print(c1.size)

    print("remove top")
    print(c1.pop_top())
    print(c1)
    print("remove tail")
    print(c1.pop_tail())
    print(c1)

    print()
    c = CycleDoubleConnected()
    print(c)
    for i in range(1, 30, 5):
        c.push_tail(DoubleNode(i)) if i % 2 else c.push_top(DoubleNode(i))
    print(c)
    print()
    print("add 55 at index 10")
    try:
        c.push_n(10, DoubleNode(55))
        print(c)
    except IndexError:
        print(f'А вот не получится запушить элемент на 11 позицию, когда в списке {c.size} элементов')
    print("add 100 at index 1")
    c.push_n(1, DoubleNode(100))
    print(c)
    print()
    print("remove top")
    print(c.pop_top())
    print(c)
    print("remove tail")
    print(c.pop_tail())
    print(c)
    print()
    print("remove 100")
    print(c.pop_content(DoubleNode(100)))
    print(c)
    print()
    try:
        print("remove 29")
        print(c.pop_content(DoubleNode(29)))
        print(c)
    except ValueError:
        print("А нету в списке того, что хочется удалить...")
    print()
    print(c.pop_content(DoubleNode(16)))
    print("remove 16")
    print(c)

    try:
        print(c.pop_n(10))
        print("remove element at index 10")
    except IndexError:
        print(f"А вот не получится удалить из списка 11-ый элемент, когда в нем {c.size} элементов.")

    print(c.pop_n(2))
    print("remove element at index 2")
    print(c)

    print(c.pop_n(1))
    print("remove element at index 1")
    print(c)

    print("finding node with content 21")
    print(c.find_node_content(DoubleNode(21)))

    print("finding node at index 0")
    print(c.find_n_node(0))
