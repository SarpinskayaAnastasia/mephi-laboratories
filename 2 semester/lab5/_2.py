import sys

sys.setrecursionlimit(100000)

'''
CHATGPT ТУПОЙ УБЛЮДОК ОН НЕ УМЕЕТ КОДИТЬ МРАЗЬ ТУПОРЫЛАЯ
СЕЙЧАС Я НАПИШУ ВЕСЬ КОД И ТОГДА ВОСТОРЖЕСТВУЕТ НАТУРАЛЬНЫЙ ИНТЕЛЛЕКТ
ДА ЗДРАВСТВУЕТ НАТУРАЛЬНЫЙ ИНТЕЛЛЕКТ
'''


def bin_search(arr, key, low, high):  # В этом есть необходимость, поскольку если функция вдруг выбросит -1,
    # ничего не получится, а low == 0 нам не факт, что подойдет
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1
    return low


def bin_paste_sort(arr: list):
    n = len(arr)
    for i in range(1, n):
        j = i - 1
        key = arr[i]
        k = bin_search(arr, key, 0, j)

        # Сдвигаем элементы вправо
        while j >= k:
            arr[j + 1] = arr[j]
            j -= 1

        arr[k] = key  # Вставляем элемент на нужное место


if __name__ == "__main__":
    arr = [3, 4, 5, 6, 3, 3, 2, 53443, 23, 436, 7, 56, 24, 24, 24, 7, 624, 534, 542422, 3, 4, 35, 63, 2]
    print(f'before: {arr}')
    bin_paste_sort(arr)
    print(f'after: {arr}')
