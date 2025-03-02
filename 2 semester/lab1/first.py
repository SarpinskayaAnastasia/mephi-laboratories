class Node:
    def __init__(cls, content):
        cls.content = content

        cls.prev = None
        cls.next = None

    def __str__(cls):
        return str(cls.content)


class Deque:
    def __init__(cls):
        cls.size = 0

        cls.front = None  # Либо None, либо Node
        cls.rear = None  # Либо None, либо Node

    def check(function):
        """Проверить, не пустой ли дек."""

        def wrapper(cls, *args, **kwargs):
            if not cls.size:
                raise IndexError("Deque is empty")
            return function(cls, *args, **kwargs)

        return wrapper

    @check
    def peek_front(cls):
        return cls.front.content

    @check
    def peek_rear(cls):
        return cls.rear.content

    @check
    def pop_front(cls):
        content = cls.front.content

        if cls.size == 1:
            cls.front = None
            cls.rear = None
        else:
            candidate = cls.front.prev

            cls.front = candidate
            candidate.next = None

        cls.size -= 1

        if cls.size == 1:
            cls.front.prev = None
            cls.front.next = None
        return content

    @check
    def pop_rear(cls):
        content = cls.rear.content

        if cls.size == 1:
            cls.front = None
            cls.rear = None
        else:
            candidate = cls.rear.next

            cls.rear = candidate
            candidate.prev = None

        cls.size -= 1

        if cls.size == 1:
            cls.rear.prev = None
            cls.rear.front = None
        return content

    def push_front(cls, _item):
        candidate = Node(_item)

        if cls.size:
            candidate.prev = cls.front
            cls.front.next = candidate

            if cls.size == 1:
                cls.front.prev = None

        cls.front = candidate
        if not cls.size:
            cls.rear = candidate

        cls.size += 1

    def push_rear(cls, _item):
        candidate = Node(_item)

        if cls.size:
            cls.rear.prev = candidate
            candidate.next = cls.rear

            if cls.size == 1:
                cls.rear.next = None

        cls.rear = candidate
        if not cls.size:
            cls.front = candidate

        cls.size += 1


def string_to_deque(string: str) -> Deque:
    deque = Deque()
    for item in string.replace(" ", "").lower():
        deque.push_rear(item)
    return deque


def is_palindrome(string: str) -> bool:
    return all(
        s.pop_rear() == s.pop_front()
        for s in [string_to_deque(string)]
        for _ in range(s.size >> 1)
    )


def main():
    print(is_palindrome("А роза упала на лапу Азора"))
    print(is_palindrome("топот"))
    print(is_palindrome("Python"))
    print(is_palindrome("12321"))


if __name__ == "__main__":
    main()
