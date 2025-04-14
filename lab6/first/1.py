def merge_sort(array):
    if len(array) <= 1:
        return array

    # Разделение массива
    mid = len(array) // 2
    left = merge_sort(array[:mid])
    right = merge_sort(array[mid:])

    # Слияние двух отсортированных частей
    return merge(left, right)


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


# Пример использования
array = [38, 27, 43, 3, 9, 82, 10]
sorted_array = merge_sort(array)
print("Отсортированный массив:", sorted_array)
