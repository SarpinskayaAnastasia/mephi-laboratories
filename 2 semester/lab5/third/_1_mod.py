def cycle_bin_srch(arr: list, x: int, l=0, r=None):
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
