class Deque:
    def __init__(self):
        self.items = []

    def empty(self) -> bool:
        return len(self.items) == 0

    def push_back(self, item):
        self.items.append(item)

    def push_front(self, item):
        self.items.insert(0, item)

    def pop_back(self):
        if self.empty():
            raise IndexError("Deque is empty")
        return self.items.pop()

    def pop_front(self):
        if self.empty():
            raise IndexError("Deque is empty")
        return self.items.pop(0)

    def length(self) -> int:
        return len(self.items)


def is_palindrome(string: str) -> bool:
    de = Deque()
    for ch in string.lower().replace(' ', ''):
        de.push_back(ch.lower())
    while de.length() > 1:
        if de.pop_front() != de.pop_back():
            return False
    return True


if __name__ == "__main__":
    print(is_palindrome("А роза упала на лапу Азора"))
