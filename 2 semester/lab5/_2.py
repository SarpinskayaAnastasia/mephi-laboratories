'''
CHATGPT ТУПОЙ УБЛЮДОК ОН НЕ УМЕЕТ КОДИТЬ МРАЗЬ ТУПОРЫЛАЯ
СЕЙЧАС Я НАПИШУ ВЕСЬ КОД И ТОГДА ВОСТОРЖЕСТВУЕТ НАТУРАЛЬНЫЙ ИНТЕЛЛЕКТ
ДА ЗДРАВСТВУЕТ НАТУРАЛЬНЫЙ ИНТЕЛЛЕКТ
'''


def bin_search(arr: list, key, l: int, r: int) -> int:  # В этом есть необходимость
    while l <= r:
        mid = (l + r) // 2
        if arr[mid] < key:
            l = mid + 1
        else:
            r = mid - 1
    return l


def bin_paste_sort(arr: list):
    n = len(arr)
    for i in range(1, n):
        j = i - 1
        key = arr[i]
        k = bin_search(arr, key, 0, j)

        while j >= k:
            arr[j + 1] = arr[j]
            j -= 1

        arr[k] = key


if __name__ == "__main__":
    arr = [3, 4, 5, 6, 3, 3, 2, 53443, 23, 436, 7, 56, 24, 24, 24, 7, 624, 534, 542422, 3, 4, 35, 63, 2]
    print(f'before: {arr}')
    bin_paste_sort(arr)
    print(f'after: {arr}')
