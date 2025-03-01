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
        return str(self.top) + ' -> ' + str(self.top.next)

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
            '''print(f"{old_tail} -> {old_tail.next}")
            print(f"{new_tail} -> {new_tail.next}")'''
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
            '''print(f"{n_1} -> {n_1.next}")
            print(f"{new_n} -> {new_n.next}")
            print(f"{old_n} -> {old_n.next}")'''
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
        # print(f"before: {need_node_n1} -> {need_node_n1.next}")
        need_node_n1.set_next(need_node.next)
        need_node.set_next(None)  # обрываем связи, чтобы действительно удалить узел
        self.size -= 1
        # print(f"after: {need_node_n1} -> {need_node_n1.next}")
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
    for i in range(1, 20, 4):
        p.push_tail(i)
    p.push_tail(77)

    p.push_n(4, 99)
    print()
    print(p.pop_top())
    print(p)
    print(p.pop_tail())
    print(p)
    print(p.pop_tail())
    print()
    print(p)
    print(p.pop_content(5))
    try:
        print(p.pop_content(8888))
    except ValueError:
        print('нету 8888...')
    print(p.size, 'size!')
    print(p.find_tail())
    print(p.top)
    print(p.find_n_node(1, True))
    print(p.find_node_content(9, True))
