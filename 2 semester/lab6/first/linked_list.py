class OnceNode:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return f"{"{"}{str(self.data)}{"}"}"

    def __eq__(self, other):
        if isinstance(other, OnceNode):
            return self.data == other.data
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, OnceNode):
            return self.data != other.data
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, OnceNode):
            return self.data < other.data
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, OnceNode):
            return self.data > other.data
        return NotImplemented


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(func):
        def wrapper(self, *args, **kwargs):
            if not self.size:
                raise IndexError("The list is empty")
            return func(self, *args, **kwargs)

        return wrapper

    @is_empty
    def __find_tail(self) -> OnceNode:
        tail = self.head
        while tail.next:
            tail = tail.next
        return tail

    def __push_top(self, content):
        new_top = OnceNode(content)
        new_top.next = self.head
        self.head = new_top
        self.size += 1

    def append(self, content):
        new_tail = OnceNode(content)
        try:
            old_tail = self.__find_tail()
            old_tail.next = new_tail
            self.size += 1
        except IndexError:
            self.__push_top(content)
