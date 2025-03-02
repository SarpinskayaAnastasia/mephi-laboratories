from frst import OnceNode, OnceConnected


def get_middle(top: OnceNode) -> OnceNode:
    slow_cursor = top
    fast_cursor = top
    while fast_cursor is not None and fast_cursor.next is not None:
        slow_cursor = slow_cursor.next
        fast_cursor = fast_cursor.next.next
    return slow_cursor.next if fast_cursor else slow_cursor  # когда в списке четное количество узлов, быстрый курсор
    # становится None, а когда нечетное - это все еще узел.


def reverse(top: OnceNode) -> OnceNode:
    prev = None  # это будет конец изначального списка и начало нового, перевернутого
    curr = top
    while curr is not None:
        nxt = curr.next
        curr.set_next(prev)
        prev = curr
        curr = nxt
    return prev


def is_palindrome(left: OnceNode) -> bool:
    if not isinstance(left, OnceNode):
        raise TypeError(f"Incorrect type of variable, expected {OnceNode}, given {type(left)}")
    if left.next is None:
        return True  # ну это если мы единственный символ считаем палиндромом, разумеется
    scnd_half = get_middle(left)
    right = reverse(scnd_half)
    while right is not None:
        if right != left:  # это стало возможным, потому что в классе узла мы прописали сравнения
            return False
        right = right.next
        left = left.next
    return True


def gen_case(string: str) -> tuple[OnceNode, bool]:
    string = string.replace(' ', '').lower()
    temp = OnceConnected()
    for n in string:
        temp.push_top(n)
    return temp.top, string == string[::-1]


if __name__ == "__main__":
    cases = []
    for w in ['12321', '123321', '1', '11', 'А роза упала на лапу Азора', 'gegwg', 'some word...']:
        cases.append(gen_case(w))
    for input_top, verdict in cases:
        assert (is_palindrome(input_top) == verdict), f"Case failed for {input_top}, expected {str(verdict)}"
    print("All unit tests passed")
