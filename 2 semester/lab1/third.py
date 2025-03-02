class SuperStack:
    def __init__(cls, n: int, threshold: int):
        if not isinstance(n, int) or n < 1:
            raise ValueError("Amount of stacks must be a natural number")
        cls.n = n

        if not isinstance(threshold, int) or threshold < 1:
            raise ValueError("Array threshold must be a natural number")
        cls.threshold = threshold

        cls.buffers = list()
        cls.bonds = list()

    def check_if_bad_n(function):
        """Проверить, корректен ли номер стека."""

        def wrapper(cls, *args, **kwargs):
            n = args[0]
            if not isinstance(n, int) or n in range(n):
                raise IndexError("No stacks found under such index")
            return function(cls, *args, **kwargs)

        return wrapper

    def check_if_empty(function):
        """Проверить, не пустой ли стек."""

        def wrapper(cls, *args, **kwargs):
            n = args[0]
            if n not in cls.bonds:
                raise IndexError("Stack is empty")
            return function(cls, *args, **kwargs)

        return wrapper

    @check_if_bad_n
    @check_if_empty
    def peek(cls, n: int):
        return cls.buffers[cls.bonds.index(n)]

    @check_if_bad_n
    @check_if_empty
    def pop(cls, n: int):
        index = cls.bonds.index(n)
        cls.bonds.pop(index)
        return cls.buffers.pop(index)

    @check_if_bad_n
    def push(cls, n: int, item):
        if len(cls.buffers) == cls.threshold:
            raise OverflowError("Stacks are full")
        cls.bonds.insert(0, n)
        cls.buffers.insert(0, item)


def main():
    fruits = SuperStack(n=6, threshold=24)

    fruits.push(4, "apple")
    fruits.push(4, "orange")
    fruits.push(2, "banana")

    print(fruits.peek(2))
    print(fruits.pop(4))
    print(fruits.peek(4))

    drinks = SuperStack(n=2, threshold=1)

    drinks.push(0, "green_tea")
    print(drinks.pop(0))
    drinks.push(0, "oolong")
    try:
        drinks.push(1, "americano")
    except OverflowError:
        print("Can't push more")


if __name__ == "__main__":
    main()
