def merge(left, right):
    result = []
    i = j = 0
    # Сравнение элементов и объединение
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Добавление оставшихся элементов
    result.extend(left[i:])
    result.extend(right[j:])

    return result


def merge_sort(array):
    if len(array) <= 1:
        return array

    # Разделение массива
    mid = len(array) // 2
    left = merge_sort(array[:mid])
    right = merge_sort(array[mid:])

    # Слияние двух отсортированных частей
    return merge(left, right)



def partition(arr, low, high):
    # Опорный элемент — первый в текущем подмассиве
    pivot = arr[low]
    i = low + 1  # Граница для элементов меньше pivot

    for j in range(low + 1, high + 1):
        # Если текущий элемент меньше pivot, меняем местами с элементом на границе
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    # Помещаем pivot на правильную позицию
    arr[low], arr[i - 1] = arr[i - 1], arr[low]
    return i - 1  # Возвращаем индекс pivot


def quicksort(arr, low, high):
    if low < high:
        # pi — индекс опорного элемента после разбиения
        pi = partition(arr, low, high)
        # Рекурсивно сортируем элементы до и после опорного
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)
