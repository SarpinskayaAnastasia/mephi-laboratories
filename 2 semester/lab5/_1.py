def cycle_bin_srch(arr: list, index: int):
    left = 0
    right = len(arr)-1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == index:
            return mid
        elif arr[mid] < index:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def rec_bin_srch(arr: list, x: int, l=0, r=None):
    if r is None:  # первая обработка значений в самом-самом начале
        r = len(arr) - 1  # три сценария: либо n > 1, либо n == 1, либо n == 0
        if not r:
            if x == arr[r]:
                return r
            else:
                return -1
        elif r == -1:
            raise ValueError("Array is empty")
    current = (l + r) // 2
    if arr[current] == x:
        return current
    elif arr[current] > x:
        return rec_bin_srch(arr, x, l, current - 1)
    else:
        return rec_bin_srch(arr, x, current + 1, r)


if __name__ == "__main__":
    array = sorted([3, 5435, 23, 45, 2, 3, 5, 3, 2, 5, 67, 7, 54, 3, 24, 6, 7, 4, 3, 66, 4, 2, 4, 6, 4, 43, 5, 55])
    print(rec_bin_srch(array, 54, 0, len(array)), array.index(54))
    arr = [1]
    print(rec_bin_srch(arr, 1))
    print(rec_bin_srch(arr, 5))
    urr = []
    try:
        print(rec_bin_srch(urr, 99))
    except ValueError:
        print(-1)

    print(cycle_bin_srch(array, 54))
