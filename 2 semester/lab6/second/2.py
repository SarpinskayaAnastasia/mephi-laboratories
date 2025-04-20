import random
import time


class MergeSort:
    @staticmethod
    def sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = MergeSort.sort(arr[:mid])
        right = MergeSort.sort(arr[mid:])
        return MergeSort._merge(left, right)

    @staticmethod
    def _merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result


class QuickSort:
    @staticmethod
    def sort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return QuickSort.sort(left) + middle + QuickSort.sort(right)


class OptimizedQuickSort:
    @staticmethod
    def sort_median(arr):
        if len(arr) <= 20:
            return OptimizedQuickSort._insertion_sort(arr)
        pivot = OptimizedQuickSort._median_of_three(arr)
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return OptimizedQuickSort.sort_median(left) + middle + OptimizedQuickSort.sort_median(right)

    @staticmethod
    def sort_random(arr):
        if len(arr) <= 20:
            return OptimizedQuickSort._insertion_sort(arr)
        pivot = arr[random.randint(0, len(arr) - 1)]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return OptimizedQuickSort.sort_random(left) + middle + OptimizedQuickSort.sort_random(right)

    @staticmethod
    def _insertion_sort(arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    @staticmethod
    def _median_of_three(arr):
        a, b, c = arr[0], arr[len(arr) // 2], arr[-1]
        return a + b + c - max(a, b, c) - min(a, b, c)


class InPlaceMergeSort:
    @staticmethod
    def sort(arr):
        InPlaceMergeSort._merge_sort(arr, 0, len(arr) - 1)

    @staticmethod
    def _merge_sort(arr, l, r):
        if l >= r:
            return
        mid = (l + r) // 2
        InPlaceMergeSort._merge_sort(arr, l, mid)
        InPlaceMergeSort._merge_sort(arr, mid + 1, r)
        if arr[mid] <= arr[mid + 1]:
            return
        InPlaceMergeSort._merge(arr, l, mid, r)

    @staticmethod
    def _merge(arr, l, mid, r):
        left = arr[l:mid + 1]
        right = arr[mid + 1:r + 1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1


def benchmark(sizes):
    line = "-" * 40
    header = f"{'Метод':30} | Время (мс)"

    def run_algorithms(title, algorithms):
        print(f"\n{title}:\n{line}\n{header}\n{line}")
        for name, func, copy_data in algorithms:
            data = arr.copy() if copy_data else arr
            t0 = time.time()
            func(data)
            print(f"{name:<30} | {(time.time() - t0) * 1000:.2f}")
        print(line)

    std = [
        ("Сортировка слиянием", MergeSort.sort, True),
        ("Быстрая сортировка", QuickSort.sort, True),
        ("Python sorted()", sorted, True),
    ]
    opt = [
        ("QuickSort (медиана трёх)", OptimizedQuickSort.sort_median, True),
        ("QuickSort (случайный pivot)", OptimizedQuickSort.sort_random, True),
        ("In-place Merge Sort", InPlaceMergeSort.sort, False),
    ]

    for size in sizes:
        arr = [random.randint(-10000, 10000) for _ in range(size)]
        print(f"\nРазмер массива: {size}")
        run_algorithms("Обычные версии", std)
        run_algorithms("Оптимизированные версии", opt)


if __name__ == "__main__":
    sizes = [10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6]
    benchmark(sizes)
