def bin_search(arr: list, key_val, l: int, r: int, key=lambda x: x) -> int:
    while l <= r:
        mid = (l + r) // 2
        if key(arr[mid]) < key_val:
            l = mid + 1
        else:
            r = mid - 1
    return l


def bin_paste_sort(arr: list, key=lambda x: x):
    n = len(arr)
    for i in range(1, n):
        current = arr[i]
        key_val = key(current)
        insert_pos = bin_search(arr, key_val, 0, i - 1, key)

        for j in range(i, insert_pos, -1):
            arr[j] = arr[j - 1]

        arr[insert_pos] = current
