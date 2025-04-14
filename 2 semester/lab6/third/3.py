def natural_merge_sort(array):
    comparisons = [0]  # Используем список для mutable counter внутри функций

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons[0] += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    if len(array) <= 1:
        return array, 0

    # Находим все возрастающие подпоследовательности (run)
    runs = []
    start = 0
    for i in range(1, len(array)):
        comparisons[0] += 1
        if array[i] < array[i - 1]:
            runs.append(array[start:i])
            start = i
    runs.append(array[start:])

    # Сливаем пары runs, пока не останется один
    while len(runs) > 1:
        new_runs = []
        for i in range(0, len(runs), 2):
            if i + 1 < len(runs):
                new_runs.append(merge(runs[i], runs[i + 1]))
            else:
                new_runs.append(runs[i])
        runs = new_runs

    return runs[0], comparisons[0]


# Модифицируем оригинальные функции для подсчета сравнений
def merge_sort_with_count(array):
    comparisons = [0]

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons[0] += 1
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def _merge_sort(array):
        if len(array) <= 1:
            return array
        mid = len(array) // 2
        left = _merge_sort(array[:mid])
        right = _merge_sort(array[mid:])
        return merge(left, right)

    sorted_array = _merge_sort(array)
    return sorted_array, comparisons[0]


def quicksort_with_count(arr):
    comparisons = [0]

    def partition(low, high):
        pivot = arr[low]
        i = low + 1
        for j in range(low + 1, high + 1):
            comparisons[0] += 1
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[low], arr[i - 1] = arr[i - 1], arr[low]
        return i - 1

    def _quicksort(low, high):
        if low < high:
            pi = partition(low, high)
            _quicksort(low, pi - 1)
            _quicksort(pi + 1, high)

    _quicksort(0, len(arr) - 1)
    return arr, comparisons[0]


# Функция для сравнения производительности
def compare_sorts(array_size=1000, array_type='random'):
    import random

    # Генерируем массив в зависимости от типа
    if array_type == 'random':
        arr = [random.randint(0, 10000) for _ in range(array_size)]
    elif array_type == 'sorted':
        arr = [i for i in range(array_size)]
    elif array_type == 'reverse':
        arr = [i for i in range(array_size, 0, -1)]

    # Создаем копии для каждого алгоритма
    arr1 = arr.copy()
    arr2 = arr.copy()
    arr3 = arr.copy()

    # Выполняем сортировки
    _, natural_comparisons = natural_merge_sort(arr1)
    _, merge_comparisons = merge_sort_with_count(arr2)
    _, quick_comparisons = quicksort_with_count(arr3)

    print(f"Array type: {array_type}, size: {array_size}")
    print(f"Natural merge sort comparisons: {natural_comparisons}")
    print(f"Classic merge sort comparisons: {merge_comparisons}")
    print(f"Quick sort comparisons: {quick_comparisons}")
    print("-" * 50)


# Пример использования
if __name__ == "__main__":
    # Сравниваем для разных типов массивов
    for size in [1000, 5000, 10000]:
        for array_type in ['random', 'sorted', 'reverse']:
            compare_sorts(size, array_type)
