def bin_search(arr: list, key_val, l: int, r: int, key=lambda x: x) -> int:  # здесь мы ищем не индекс искомого
    # элемента, а индекс, куда нужно вставить этот элемент!
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


if __name__ == "__main__":
    arr = [3, 4, 5, 6, 3, 3, 2, 53443, 23, 436, 7, 56, 24, 24, 24, 7, 624, 534, 542422, 3, 4, 35, 63, 2]
    print(f'before: {arr}')
    bin_paste_sort(arr)
    print(f'after: {arr}')
