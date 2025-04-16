"""вооот"""
import random
import time
import sys
from statistics import median

sys.setrecursionlimit(1000000)

def generate_random_array(size):
    return [random.randint(-10000, 10000) for _ in range(size)]

# --- Стандартные алгоритмы ---
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
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


def quick_sort(array):
    if len(array) <= 1:
        return array
    pivot = array[len(array) // 2]  
    left = [x for x in array if x < pivot]  
    middle = [x for x in array if x == pivot]  
    right = [x for x in array if x > pivot]  
    return quick_sort(left) + middle + quick_sort(right)


# --- Оптимизированные версии ---
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Быстрая сортировка с разными стратегиями выбора pivot
def median_of_three(arr):
    first, mid, last = arr[0], arr[len(arr)//2], arr[-1]
    return median([first, mid, last])

def quick_sort_median(arr):
    if len(arr) <= 20:
        return insertion_sort(arr)
    pivot = median_of_three(arr)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_median(left) + middle + quick_sort_median(right)

def quick_sort_random(arr):
    if len(arr) <= 20:
        return insertion_sort(arr)
    pivot = arr[random.randint(0, len(arr)-1)]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_random(left) + middle + quick_sort_random(right)

# In-place Merge Sort (по времени НЕ ОЧЕНЬ) 
# ((Избегание копирования при слиянии, работаем с исходным массивом, передавая индексы, вместо создания новых массивов
def inplace_merge_sort(arr, l=0, r=None):
    if r is None:
        r = len(arr) - 1
    if l >= r:
        return
    mid = (l + r) // 2
    inplace_merge_sort(arr, l, mid)
    inplace_merge_sort(arr, mid + 1, r)
    # Оптимизация: если подмассивы уже упорядочены, слияние не нужно
    if arr[mid] <= arr[mid + 1]:
        return
    inplace_merge(arr, l, mid, r)

def inplace_merge(arr, l, mid, r):
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


# --- Бенчмарк ---
def benchmark(sizes):
    for size in sizes:
        arr = generate_random_array(size)
        print(f"\nРазмер массива: {size}")
        print("---------------------------------")
        print("Метод                       | Время (мс)")
        print("---------------------------------")
        
        # Стандартные алгоритмы
        arr_copy = arr.copy()
        start = time.time()
        merge_sort(arr_copy)
        merge_time = (time.time() - start) * 1000
        print(f"Сортировка слиянием         | {merge_time:.2f}")
        
        arr_copy = arr.copy()
        start = time.time()
        quick_sort(arr_copy)
        quick_time = (time.time() - start) * 1000
        print(f"Быстрая сортировка          | {quick_time:.2f}")
        
        arr_copy = arr.copy()
        start = time.time()
        sorted(arr_copy)
        python_time = (time.time() - start) * 1000
        print(f"Python sorted()             | {python_time:.2f}")
        print("---------------------------------")
        
        # Оптимизированные алгоритмы
        print("\n\nОптимизированные версии:")
        print("---------------------------------")
        print("Метод                       | Время (мс)")
        print("---------------------------------")
        
        arr_copy = arr.copy()
        start = time.time()
        quick_sort_median(arr_copy)
        qs_median_time = (time.time() - start) * 1000
        print(f"QuickSort (медиана трёх)    | {qs_median_time:.2f}")
        
        arr_copy = arr.copy()
        start = time.time()
        quick_sort_random(arr_copy)
        qs_random_time = (time.time() - start) * 1000
        print(f"QuickSort (случайный pivot) | {qs_random_time:.2f}")
        
        arr_copy = arr.copy()
        start = time.time()
        inplace_merge_sort(arr_copy)
        inplace_merge_time = (time.time() - start) * 1000
        print(f"In-place Merge Sort         | {inplace_merge_time:.2f}")
        print("---------------------------------")

if __name__ == "__main__":
    sizes = [10**3, 10**4, 10**5, 10**6]
    benchmark(sizes)
