from sys import setrecursionlimit
import random

from originals import merge, merge_sort, quicksort

setrecursionlimit(10000000)


def natural_merge_sort(array):
    comparisons = 0
    n = len(array)

    # Найти все естественные отсортированные подмассивы
    def find_runs(array):
        runs = []
        start = 0
        for i in range(1, n):
            if array[i] < array[i - 1]:
                runs.append(array[start:i])
                start = i
        runs.append(array[start:])
        return runs

    def merge_runs(runs):
        nonlocal comparisons
        while len(runs) > 1:
            new_runs = []
            for i in range(0, len(runs), 2):
                if i + 1 < len(runs):
                    left = runs[i]
                    right = runs[i + 1]
                    merged, count = merge(left, right)
                    comparisons += count
                    new_runs.append(merged)
                else:
                    new_runs.append(runs[i])
            runs = new_runs
        return runs[0]

    runs = find_runs(array)
    sorted_array = merge_runs(runs)
    return sorted_array, comparisons


def compare_sorts(size: int):
    results = []

    random_arr = [random.randint(-10000, 10000) for _ in range(size)]
    sorted_arr = sorted(random_arr)
    reversed_arr = sorted_arr[::-1]

    # Сравниваем каждый алгоритм
    for arr_type, arr in [("Случайный", random_arr), ("Отсортированный", sorted_arr), ("Обратный", reversed_arr)]:
        sorted_array, natural_comparisons = natural_merge_sort(arr[:])

        merge_sorted, merge_comparisons = merge_sort(arr[:])

        quick_comparisons = quicksort(arr[:], 0, len(arr) - 1)

        results.append((
            arr_type,
            natural_comparisons, merge_comparisons, quick_comparisons
        ))

    print(f"{'Тип массива':20} | Natural Merge | Classic Merge | Quick Sort")
    for result in results:
        print(f"{result[0]:20} | {result[1]:<13} | {result[2]:<13} | {result[3]:<10}")
    print('-' * 80)


if __name__ == "__main__":
    sizes = [1001, 5001, 10001]
    print('-' * 80)
    for size in sizes:
        compare_sorts(size)
