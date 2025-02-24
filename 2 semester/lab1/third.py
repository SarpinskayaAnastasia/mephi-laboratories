class NStacks:
    def __init__(self, n: int, capacity: int):
        self.n = n
        self.capacity = capacity
        self.tops = [-1] * n
        self.stacks = []
        for _ in range(n):
            self.stacks.append([None] * capacity)

    def __str__(self):
        return f'self.tops: {self.tops}\nself.stacks: {self.stacks}'

    def pusho(self, index, item):
        if index not in range(self.n):
            raise IndexError(f"Stack with index {index} doesn't exist.")
        if self.tops[index] == self.capacity - 1:
            raise OverflowError(f"Stack with index {index} is full.")
        self.tops[index] += 1
        self.stacks[index][self.tops[index]] = item

    def popo(self, index):
        if index not in range(self.n):
            raise IndexError(f"Stack with index {index} doesn't exist.")
        if self.tops[index] == -1:
            raise IndexError(f"Pop from the empty stack with index {index}")
        item = self.stacks[index][self.tops[index]]
        self.stacks[index][self.tops[index]] = None
        self.tops[index] -= 1
        return item

    def get_items(self, index):
        if index not in range(self.n):
            raise IndexError(f"Stack with index {index} doesn't exist.")
        return self.stacks[index]


if __name__ == "__main__":
    ouo = NStacks(5, 4)
    for _ in range(4):
        ouo.pusho(1, 7)
    ouo.popo(1)
    print(ouo)
