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
            return self.data == other.data and self.next == other.next and self.prev == other.next
        return NotImplemented

    def set_next_prev(self, node_n, node_p):
        self.next = node_n
        self.prev = node_p


class OnceConnected:
    def __init__(self):
        self.top = None
        self.size = 0

    def __str__(self):
        try:
            self.is_empty()
            s = []
            n = self.top
            while n is not None:
                s.append(str(n))
                n = n.next
            return ' -> '.join(s)
        except IndexError:
            return 'This is an empty once connected list.'

    def is_empty(self):
        if not self.size:
            raise IndexError("List is empty")

    def find_tail(self):
        self.is_empty()
        tail = self.top
        while tail.next is not None:
            tail = tail.next
        return tail

    # Что мы тут делаем? В общем, тут как бы два режима: поиск для пуша и поиск просто. В случае пуша нам удобнее
    # использовать предыдущий от искомого узел. А в случае поиска нам нужен именно тот, который ищем)
    def find_n_node(self, index, searching=False):
        self.is_empty()
        if index not in range(self.size):
            raise IndexError(f"Incorrect index, expected integer number from 0 to {self.size}")
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
    def find_node_content(self, content, searching=False):
        self.is_empty()
        if searching and self.top.data == content:
            return self.top
        elif self.size != 1 and self.top.data != content:
            prev = self.top
            res = self.top.next
            while res.data != content:
                prev = prev.next
                res = res.next
                if res is None:
                    raise ValueError(f"Node with content {content} doesn't exist")
            if searching:
                return res
            return prev
        else:
            raise ValueError(f"Node with content {content} doesn't exist")

    def push_top(self, item):  # push to top
        new_node = OnceNode(item)
        new_node.set_next(self.top)
        self.top = new_node
        self.size += 1

    def push_tail(self, item):  # push to tail
        try:
            new_tail = OnceNode(item)
            old_tail = self.find_tail()
            old_tail.set_next(new_tail)
            self.size += 1
        except IndexError:  # если список пуст, без разницы, как добавить наш элемент
            self.push_top(item)

    def push_n(self, index, item):
        if not index:
            self.push_top(item)
            return None
        try:
            new_n = OnceNode(item)
            n_1 = self.find_n_node(index)
            old_n = n_1.next
            n_1.set_next(new_n)
            new_n.set_next(old_n)
            self.size += 1
        except IndexError:
            self.push_top(item)  # то же самое

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

    def pop_content(self, content):
        self.is_empty()
        if self.top.data == content:
            return self.pop_top()
        need_node_n1 = self.find_node_content(content)
        need_node = need_node_n1.next
        need_node_n1.set_next(need_node.next)
        need_node.set_next(None)  # обрываем связи, чтобы действительно удалить узел
        self.size -= 1
        return need_node

    def pop_n(self, index):
        self.is_empty()
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
        try:
            self.is_empty()
            s = []
            n = self.top
            while n is not None:
                s.append(str(n))
                n = n.next
            return ' <-> '.join(s)
        except IndexError:
            return 'This is an empty doubly connected list.'

    def find_tail(self):
        return self.tail  # не будем использовать эту функцию, но на случай вызова лучше, чтобы она была быстрой

    def find_n_node(self, index, searching=None):  # теперь режим поиска - атавизм)
        self.is_empty()
        if index not in range(self.size):
            raise IndexError(f"Incorrect index, expected integer number from 0 to {self.size}")
        if index < self.size // 2:  # способ ускорить поиск
            res = self.top
            while index != 0:
                res = res.next
                index -= 1
        else:
            res = self.tail
            while index != 1:
                res = res.prev
                index -= 1
        return res

    def find_node_content(self, content, searching=False):
        self.is_empty()
        if self.top.data == content:
            return self.top
        elif self.tail.data == content:
            return self.tail
        elif self.size != 1:
            res = self.top.next
            while res.data != content:
                res = res.next
                if res is None:
                    raise ValueError(f"Node with content {content} doesn't exist")
            return res
        else:
            raise ValueError(f"Node with content {content} doesn't exist")

    def push_top(self, item):
        new_top = DoubleNode(item)
        if self.size:
            new_top.set_next_prev(self.top, None)
            self.top.set_next_prev(self.top.next, new_top)
            self.top = new_top
        else:
            self.top = self.tail = new_top
        self.size += 1

    def push_tail(self, item):
        new_tail = DoubleNode(item)
        if self.size:
            new_tail.set_next_prev(None, self.tail)
            self.tail.set_next_prev(new_tail, self.tail.prev)
            self.tail = new_tail
        else:
            self.top = self.tail = new_tail
        self.size += 1

    def push_n(self, index, item):
        if not index:
            self.push_top(item)
            return None
        elif index == self.size - 1:
            self.push_tail(item)
            return None
        try:
            new_n = DoubleNode(item)
            old_n = self.find_n_node(index)
            pr = old_n.prev
            new_n.set_next_prev(old_n, pr)
            pr.set_next_prev(new_n, pr.prev)
            old_n.set_next_prev(old_n.next, new_n)
            self.size += 1
        except IndexError:
            self.push_top(item)

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

    def pop_content(self, content):
        self.is_empty()
        if self.top.data == content:
            return self.pop_top()
        elif self.tail.data == content:
            return self.pop_tail()
        need_node = self.find_node_content(content)
        pr = need_node.prev
        nx = need_node.next
        pr.set_next_prev(nx, pr.prev)
        nx.set_next_prev(nx.next, pr)
        need_node.set_next_prev(None, None)
        self.size -= 1
        return need_node

    def pop_n(self, index):
        self.is_empty()
        if not index:
            return self.pop_top()
        elif index == self.size - 1:
            return self.pop_tail()
        need_node = self.find_n_node(index)
        pr = need_node.prev
        nx = need_node.next
        pr.set_next_prev(nx, pr.prev)
        nx.set_next_prev(nx.next, pr)
        need_node.set_next_prev(None, None)
        self.size -= 1
        return need_node


class CycleDoubleConnected(DoubleConnected):
    def __str__(self):
        if self.size:
            s = []
            n = self.top
            while not n == self.tail:
                s.append(str(n))
                n = n.next
            return '-> ' + ' <-> '.join(s) + ' ->'
        else:
            return 'This is an empty circular doubly connected list.'

    def make_cycle(self):
        self.is_empty()
        if not (self.top.prev and self.tail.next):
            self.top.set_next_prev(self.top.next, self.tail)
            self.tail.set_next_prev(self.top, self.tail.prev)

    def push_top(self, item):
        new_top = DoubleNode(item)
        if not self.size:
            self.top = self.tail = new_top
            self.make_cycle()
        else:
            new_top.set_next_prev(self.top, self.tail)
            self.top.set_next_prev(self.top.next, new_top)
            self.tail.set_next_prev(new_top, self.tail.prev)
            self.top = new_top
        self.size += 1

    def push_tail(self, item):  # в циклическом списке этот вид пуша одинаков
        self.push_top(item)

    def push_n(self, index, item):  # теперь не нужно обрабатывать особые случаи
        try:
            new_n = DoubleNode(item)
            old_n = self.find_n_node(index)
            pr = old_n.prev
            new_n.set_next_prev(old_n, pr)
            pr.set_next_prev(new_n, pr.prev)
            old_n.set_next_prev(old_n.next, new_n)
            self.size += 1
        except IndexError:
            self.push_top(item)

    def pop_top(self):
        self.is_empty()

    def pop_tail(self):
        self.is_empty()

    def pop_content(self, content):
        self.is_empty()

    def pop_n(self, index):
        self.is_empty()


if __name__ == "__main__":
    p = OnceConnected()
    print(p)
    for i in range(1, 20, 4):
        p.push_tail(i)
    print(p)
    p.push_top(77)
    print(p)
    print()
    t = DoubleConnected()
    print(t)
    for i in range(1, 20, 3):
        t.push_top(i) if i % 2 else t.push_tail(i)
    print(t)
    print(t.find_node_content(7))
    print(t.pop_content(7))
    print(t)
    print(t.find_n_node(3))
    print(t.pop_n(3))
    print(t)
