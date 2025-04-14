from linked_list import LinkedList, OnceNode


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
    result = LinkedList()
    i = j = 0
    # Сравнение элементов и объединение
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    else:
        i -= 1 if i >= len(left) else 0
        j -= 1 if j >= len(right) else 0

    # Добавление оставшихся элементов
    result.extend(left[i:])
    result.extend(right[j:])

    return result


if __name__ == "__main__":
    linked_list = LinkedList()
    linked_list.append(OnceNode(38))
    linked_list.append(OnceNode(27))
    linked_list.append(OnceNode(43))
    linked_list.append(OnceNode(3))
    linked_list.append(OnceNode(9))
    linked_list.append(OnceNode(82))
    linked_list.append(OnceNode(10))
    sorted_linked_list = merge_sort(linked_list)
    print("\nОтсортированный связный список:", sorted_linked_list)
