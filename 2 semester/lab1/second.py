from third import NStacks

test_cases = [
    [[1, 2, 3, 4, 5], True],
    [[5, 4, 3, 2, 1], True],
    [[2, 1, 4, 3, 5], True],
    [[3, 2, 1, 4, 5], True],
    [[4, 3, 5, 2, 1], True],
    [[2, 3, 1, 4, 5], True],
    [[1, 3, 2, 5, 4], True],
    [[4, 5, 3, 2, 1], True],
    [[5, 3, 4, 2, 1], False],
    [[3, 1, 2, 5, 4], False],
    [[5, 1, 4, 2, 3], False],
    [[3, 5, 4, 1, 2], False],
]


def can_rearrange_cars(entering: list[int], exiting: list[int]) -> bool:
    if len(entering) != len(exiting):
        raise ValueError("The number of cars entering and exiting is different.")
    street = 0
    jail = 1
    sts = NStacks(2, len(entering))
    for fe in entering[::-1]:  # переворачиваем стек с въезжающими машинами, чтобы все корректно добавлялось в стек с
        # выезжающими машинами
        sts.pusho(street, fe)
    for lim in exiting:
        while lim in sts.get_items(street):
            itm = sts.popo(street)
            sts.pusho(jail, itm)
        if sts.popo(jail) != lim:
            return False
    return True


if __name__ == "__main__":
    enter_order = [1, 2, 3, 4, 5]
    f = True
    for exit_order, result in test_cases:
        if can_rearrange_cars(enter_order, exit_order) != result:
            print(f'fail: {exit_order}, expected: {result}')
            f = False
    if f:
        print('success')
