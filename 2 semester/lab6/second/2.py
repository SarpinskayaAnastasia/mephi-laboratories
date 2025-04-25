import random
import time
import heapq


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


class Heapify:
    '''
    @staticmethod
    def make_heap(arr):
        heap = [float('-inf')]
        for i in range(2, len(arr) + 1):
            heap.append(arr[i - 1])
            while heap[i // 2] >= heap[i]:
                heap[i // 2], heap[i] = heap[i], heap[i // 2]
        return heap

    @staticmethod
    def del_head(heap_arr):
        heap_arr[1], heap_arr[-1] = heap_arr[-1], heap_arr[1]
        deleted_item = heap_arr.pop()
        i = 1
        while 2 * i < len(heap_arr):
            if 2 * i + 1 < len(heap_arr):
                min_ind = 2 * i if heap_arr[2 * i] < heap_arr[2 * i + 1] else 2 * i + 1
            else:
                min_ind = 2 * i

            if heap_arr[i] <= heap_arr[min_ind]:
                break

            heap_arr[i], heap_arr[min_ind] = heap_arr[min_ind], heap_arr[i]
            i = min_ind

        return deleted_item

    def sort(self, arr):
        new_array = []
        heapified_array = self.make_heap(arr)
        while len(heapified_array) > 1:
            new_array.append(self.del_head(heapified_array))
        return new_array
    '''

    def heapify(self, arr, n, i):
        largest = i  # Initialize largest as root
        l = 2 * i + 1  # left = 2*i + 1
        r = 2 * i + 2  # right = 2*i + 2
        # See if left child of root exists and is
        # greater than root
        if l < n and arr[i] < arr[l]:
            largest = l
        # See if right child of root exists and is
        # greater than root
        if r < n and arr[largest] < arr[r]:
            largest = r

        # Change root, if needed
        if largest != i:
            (arr[i], arr[largest]) = (arr[largest], arr[i])  # swap
            # Heapify the root.
            self.heapify(arr, n, largest)

    def sort(self, arr):
        n = len(arr)
        # Build a maxheap.
        # Since last parent will be at (n//2) we can start at that location.
        for i in range(n // 2, -1, -1):
            self.heapify(arr, n, i)
        # One by one extract elements
        for i in range(n - 1, 0, -1):
            (arr[i], arr[0]) = (arr[0], arr[i])  # swap
            self.heapify(arr, i, 0)


class Heapify_bib:
    @staticmethod
    def sort(arr):
        heapq.heapify(arr)
        result = []
        while arr:
            result.append(heapq.heappop(arr))
        return result


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
        ("Сортировка слиянием", MergeSort().sort, True),
        ("Быстрая сортировка", QuickSort().sort, True),
        ("Python sorted()", sorted, True),
    ]
    opt = [
        ("QuickSort (медиана трёх)", OptimizedQuickSort().sort_median, True),
        ("QuickSort (случайный pivot)", OptimizedQuickSort().sort_random, True),
        ("In-place Merge Sort", InPlaceMergeSort().sort, False),
    ]

    heapify = [
        ("Heapify кастомная", Heapify().sort, False),
        ("Heapify с библиотекой", Heapify_bib().sort, False)
    ]

    for size in sizes:
        arr = [random.randint(-10000, 10000) for _ in range(size)]
        print(f"\nРазмер массива: {size}")
        run_algorithms("Обычные версии", std)
        run_algorithms("Оптимизированные версии", opt)
        run_algorithms("Пирамидальные сортировки", heapify)


if __name__ == "__main__":
    urr = [3, 4, 5, 10, 5, 9, 6, 12, 40]

    print(Heapify().sort(urr))
    sizes = [10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6]
    benchmark(sizes)
