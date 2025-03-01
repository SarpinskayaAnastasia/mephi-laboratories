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

    def set_next_prev(self, node_n, node_p):
        self.next = node_n
        self.prev = node_p


class OneConnected:
    def __init__(self):
        self.top = None
        self.size = 0

    def __str__(self):
        try:
            self.is_empty()
            s = [str(self.top)]
            n = self.top
            while n.next is not None:
                n = n.next
                s.append(str(n))
            return ' -> '.join(s)
        except IndexError:
            return 'This is an empty once connected list.'

    def is_empty(self):
        if not self.size:
            raise IndexError("Stack is empty")

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
        if index not in range(self.size):
            raise IndexError(f"Node with index {index} doesn't exist")
        if not index:
            self.push_top(item)
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
        content = self.top.data
        self.top = self.top.next
        self.size -= 1
        return content

    def pop_tail(self):
        self.is_empty()
        new_tail = self.find_n_node(self.size - 1)  # мы не ищем сам хвост, а предыдущий от него элемент
        content = new_tail.next
        new_tail.set_next(None)
        self.size -= 1
        return content

    def pop_content(self, content):
        self.is_empty()
        if self.top.data == content:
            return self.pop_top()  # если у нас один элемент в списке, и его содержание совпадает с искомым, нам без
            # разницы, как его удалять
        need_node_n1 = self.find_node_content(content)
        need_node = need_node_n1.next
        need_node_n1.set_next(need_node.next)
        need_node.set_next(None)  # обрываем связи, чтобы действительно удалить узел
        self.size -= 1
        return need_node


class DoubleConnected:
    def __init__(self):
        self.top = None
        self.size = 0

    def push_top(self, item):
        pass


class CycleOneConnected:
    def __init__(self):
        self.eshkere = None


class CycleDoubleConnected:
    def __init__(self):
        self.eshkere = None


if __name__ == "__main__":
    p = OneConnected()
    print(p)
    for i in range(1, 20, 4):
        p.push_tail(i)
    print(p)
    p.push_top(77)
    print(p)
