UNITS = (
    ([1, 2, 3, 4, 5], True),
    ([5, 4, 3, 2, 1], True),
    ([2, 1, 4, 3, 5], True),
    ([3, 2, 1, 4, 5], True),
    ([4, 3, 5, 2, 1], True),
    ([2, 3, 1, 4, 5], True),
    ([1, 3, 2, 5, 4], True),
    ([4, 5, 3, 2, 1], True),
    ([5, 3, 4, 2, 1], False),
    ([3, 1, 2, 5, 4], False),
    ([5, 1, 4, 2, 3], False),
    ([3, 5, 4, 1, 2], False),
)


class Node:
    def __init__(cls, content):
        cls.content = content
        cls.link = None

    def __str__(cls):
        return str(cls.content)


class Stack:
    def __init__(cls):
        cls.size = 0
        cls.top = None

    def check(function):
        """Проверить, не пустой ли стек."""

        def wrapper(cls, *args, **kwargs):
            if not cls.size:
                raise IndexError("Stack is empty")
            return function(cls, *args, **kwargs)

        return wrapper

    @check
    def peek(cls):
        return cls.top.content

    @check
    def pop(cls):
        content = cls.top.content
        cls.top = cls.top.link
        cls.size -= 1
        return content

    def push(cls, _item):
        item = Node(_item)
        if cls.size:
            item.link = cls.top
        cls.size += 1
        cls.top = item


def list_to_stack(order: list) -> Stack:
    stack = Stack()
    order.reverse()

    for item in order:
        stack.push(item)
    return stack


def can_rearrange_cars(in_order: list[int], out_order: list[int]) -> bool:
    street, yard = list_to_stack(list(in_order)), Stack()

    for target in out_order:
        while not yard.size or yard.peek() != target:
            if not street.size:
                break
            yard.push(street.pop())

        if yard.pop() != target:
            return False
    return True


def main():
    in_order = [1, 2, 3, 4, 5]

    for out_order, verdict in UNITS:
        assert (
            can_rearrange_cars(in_order, out_order) == verdict
        ), "Case failed for %s, expected %s" % (out_order, str(verdict).upper())
    print("All unit tests passed")


if __name__ == "__main__":
    main()
