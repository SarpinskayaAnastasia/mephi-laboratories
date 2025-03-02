from frst import OnceConnected


def reversing(top, k):
    prev = None
    curr = top
    while curr and k > 0:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
        k -= 1
    return prev


def reverse_in_groups(top, k):
    if top is None or k <= 1:
        return top

    cur = top
    k_tail = None  # конец группы, состоящей из k элементов
    new_top = None

    while cur:
        count = 0
        while count < k and cur:
            cur = cur.next
            count += 1
        if count == k:  # набрали достаточное кол-во элементов
            rev_top = reversing(top, k)
            if new_top is None:  # первый раз добавляем голову
                new_top = rev_top
            if k_tail:  # соединяем с концом предыдущей группы
                k_tail.set_next(rev_top)
            k_tail = top
            top = cur

    if k_tail:  # если остались элементы, которые не нужно разворачивать
        k_tail.set_next(top)
    return new_top if new_top else top


if __name__ == "__main__":
    sll = OnceConnected()
    for i in range(1, 7):
        sll.push_tail(i)
    print(f"Before: {sll}")

    sll.top = reverse_in_groups(sll.top, 3)
    print(f"After: {sll}")

    secnd_test = OnceConnected()
    for n in range(1, 88, 5):
        secnd_test.push_tail(n)
    print(f"Before: {secnd_test}")

    secnd_test.top = reverse_in_groups(secnd_test.top, 4)
    print(f"After: {secnd_test}")
'''
    custom_test = OnceConnected()
    for n in range(i, j, k):
        custom_test.push_top(n)
    print(f"Before: {custom_test}")
    
    custom_test.top = reverse_in_groups(custom_test.top, m)
    print(f"After: {custom_test}")
'''
