from _1 import cycle_bin_srch


'''CHATGPT ТУПОЙ УБЛЮДОК ОН НЕ УМЕЕТ КОДИТЬ МРАЗЬ ТУПОРЫЛАЯ
СЕЙЧАС Я НАПИШУ ВЕСЬ КОД И ТОГДА ВОСТОРЖЕСТВУЕТ НАТУРАЛЬНЫЙ ИНТЕЛЛЕКТ
ДА ЗДРАВСТВУЕТ НАТУРАЛЬНЫЙ ИНТЕЛЛЕКТ
'''


def bin_paste_sort(arr: list):
    for i in range(1, len(arr)):
        key = arr[i]
        position = cycle_bin_srch(arr[0:i], key)

        if position == -1:
            position = 0

        shifting = arr[i]
        for j in range(i, position):
            arr[j] = arr[j - 1]
        arr[position] = shifting
    return arr


def insertion_sort(arr: list):  # первоначальная функция
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


if __name__ == "__main__":
    arr = [3, 4, 5, 6, 3, 3, 2, 53443, 23, 436, 7, 56, 24, 24, 24, 7, 624, 534, 542422, 3, 4, 35, 63, 2]
    print(f'before: {arr}')
    print(f'after: {bin_paste_sort(arr)}')
    print(f'after2: {insertion_sort(arr)}')
