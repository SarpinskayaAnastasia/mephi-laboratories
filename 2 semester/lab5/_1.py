def cycle_bin_srch(arr: list, x: int, l=0, r=None):  # Временная сложность: O(log n); Пространственная сложность: O(1)
    if r is None:  # первая обработка значений в самом-самом начале
        r = len(arr) - 1  # три сценария: либо n > 1, либо n == 1, либо n == 0
        if not r:
            if x == arr[r]:
                return r
            else:
                return -1
        elif r == -1:
            raise ValueError("Array is empty")
    while l <= r:
        mid = (l + r) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            l = mid + 1
        else:
            r = mid - 1
    return -1


def rec_bin_srch(arr: list, x: int, l=0, r=None):  # Временная сложность: O(log n); Пространственная сложность: O(1)
    if r is None:  # первая обработка значений в самом-самом начале
        r = len(arr) - 1  # три сценария: либо n > 1, либо n == 1, либо n == 0
        if not r:
            if x == arr[r]:
                return r
            else:
                return -1
        elif r == -1:
            raise ValueError("Array is empty")
    if l > r:
        return -1
    current = (l + r) // 2
    if arr[current] == x:
        return current
    elif arr[current] > x:
        return rec_bin_srch(arr, x, l, current - 1)
    else:
        return rec_bin_srch(arr, x, current + 1, r)


if __name__ == "__main__":

    array = sorted([3, 5435, 23, 45, 2, 3, 5, 3, 2, 5, 67, 7, 54, 3, 24, 6, 7, 4, 3, 66, 4, 2, 4, 6, 4, 43, 5, 55])

    print("rec_bin_srch")

    print(rec_bin_srch(array, 54), "Проверка:", array.index(54))

    print(rec_bin_srch(array, 1000))

    print(rec_bin_srch(array, array[-1]), "Проверка:", len(array) - 1)

    arr = [1]
    print(rec_bin_srch(arr, 1))

    print(rec_bin_srch(arr, 5))

    urr = []
    try:
        print(rec_bin_srch(urr, 99))
    except ValueError:
        print('SHEESH')

    print("\ncycle_bin_srch")
    print(cycle_bin_srch(array, 54))

    print(cycle_bin_srch(array, 1000))

    print(cycle_bin_srch(array, array[-1]))

    print(cycle_bin_srch(arr, 1))

    print(cycle_bin_srch(arr, 5))

    try:
        print(cycle_bin_srch(urr, 99))
    except ValueError:
        print('SHEESH')
