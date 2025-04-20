def merge(left, right):
    result = []
    i = j = 0
    comparisons = 0  # Счётчик сравнений
    # Сравнение элементов и объединение
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Добавление оставшихся элементов
    result.extend(left[i:])
    result.extend(right[j:])

    return result, comparisons


def merge_sort(array):
    comparisons = 0
    if len(array) <= 1:
        return array, comparisons

    # Разделение массива
    mid = len(array) // 2
    left, left_comparisons = merge_sort(array[:mid])
    right, right_comparisons = merge_sort(array[mid:])

    comparisons += left_comparisons + right_comparisons
    merged, merge_comparisons = merge(left, right)  # Слияние двух отсортированных частей
    comparisons += merge_comparisons

    return merged, comparisons


def partition(arr, low, high):
    comparisons = 0
    # Опорный элемент — первый в текущем подмассиве
    pivot = arr[low]
    i = low + 1  # Граница для элементов меньше pivot

    for j in range(low + 1, high + 1):
        # Если текущий элемент меньше pivot, меняем местами с элементом на границе
        comparisons += 1
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    # Помещаем pivot на правильную позицию
    arr[low], arr[i - 1] = arr[i - 1], arr[low]
    return i - 1, comparisons


def quicksort(arr, low, high):
    comparisons = 0
    if low < high:
        # pi — индекс опорного элемента после разбиения
        pi, pi_comparisons = partition(arr, low, high)
        comparisons += pi_comparisons
        # Рекурсивно сортируем элементы до и после опорного
        left_comparisons = quicksort(arr, low, pi - 1)
        right_comparisons = quicksort(arr, pi + 1, high)
        comparisons += left_comparisons + right_comparisons
    return comparisons
