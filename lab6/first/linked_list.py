class OnceNode:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return "{" + str(self.data) + "}"

    def __eq__(self, other):
        if isinstance(other, OnceNode):
            return self.data == other.data
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, OnceNode):
            return self.data != other.data
        return NotImplemented

    def set_next(self, node):
        self.next = node


class LinkedList:
    def __init__(self):
        self.top = None
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        current = self.top
        invisible_size = self.size
        while invisible_size and current:  # ну поскольку наш список не циклический, мы можем себе позволить цикл `while` instead of `for`
            yield current
            current = current.next
            invisible_size -= 1

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

    def is_n_correct(func):
        def wrapper(self, *args, **kwargs):
            if args[0] not in range(self.size):
                raise IndexError(f"Incorrect index, expected integer number from 0 to {self.size - 1}")
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
    def find_node_content(self, data: OnceNode, searching=False):
        prev = None
        for node in self:
            if node == data:
                return node if searching else prev
            prev = node
        raise ValueError(f"Node with content {data} doesn't exist")

    @is_empty
    @is_n_correct  # оба декоратора выбрасывают IndexError.
    # Но если у нас и список пустой, и индекс говно - вылезет жалоба на индекс, а не на пустой список
    def find_n_node(self, index: int, searching=False):
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

    def __getitem__(self, item):
        if isinstance(item, int):
            needed_node = self.find_n_node(item, True)
            return needed_node
        elif isinstance(item, slice):
            start, stop, step = item.indices(self.size)
            result = LinkedList()
            current_node = self.find_n_node(start, True)
            current_index = start
            while current_node and current_index < stop:
                result.append(current_node)
                current_index += step
            else:
                if current_node:
                    current_node.set_next(None)
            return result
        raise TypeError("Invalid argument type")

    def __push_top(self, node_item: OnceNode):  # push to top
        node_item.set_next(self.top)
        self.top = node_item
        self.size += 1

    def append(self, node_item: OnceNode):  # push to tail
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
    def pop_content(self, data: OnceNode) -> OnceNode:
        if self.top == data:
            return self.pop_top()
        need_node_n1 = self.find_node_content(data)
        need_node = need_node_n1.next
        need_node_n1.set_next(need_node.next)
        need_node.set_next(None)  # обрываем связи, чтобы действительно удалить узел
        self.size -= 1
        return need_node


if __name__ == "__main__":
    linked_list = LinkedList()
    linked_list.append(OnceNode(38))
    linked_list.append(OnceNode(27))
    linked_list.append(OnceNode(43))
    linked_list.append(OnceNode(3))
    linked_list.append(OnceNode(9))
    linked_list.append(OnceNode(82))
    linked_list.append(OnceNode(10))
    print(linked_list[2:5])
