from random import randint, seed


class Heap:
    def __init__(self):
        self.heap_array = []

    def __bool__(self):
        return bool(len(self.heap_array))

    def is_empty(func):
        def wrapper(self, *args, **kwargs):
            if not len(self.heap_array):
                raise IndexError("Shit!")
            return func(self, *args, **kwargs)

        return wrapper

    def push_to_heap(self, element):
        self.heap_array.append(element)
        cursor = len(self.heap_array) - 1
        while cursor > 0:
            parent = (cursor - 1) // 2
            if self.heap_array[cursor] > self.heap_array[parent]:
                return
            self.heap_array[cursor], self.heap_array[parent] = self.heap_array[parent], self.heap_array[cursor]
            cursor = parent
        return

    @is_empty
    def del_from_heap(self):
        self.heap_array[0], self.heap_array[-1] = self.heap_array[-1], self.heap_array[0]
        deleted_elem = self.heap_array.pop()
        i = 0
        while 2 * i + 1 < len(self.heap_array):
            if 2 * i + 2 < len(self.heap_array):
                min_ind = 2 * i + 1 if self.heap_array[2 * i + 1] < self.heap_array[2 * i + 2] else 2 * i + 2
            else:
                min_ind = 2 * i + 1

            if self.heap_array[i] <= self.heap_array[min_ind]:
                break

            self.heap_array[i], self.heap_array[min_ind] = self.heap_array[min_ind], self.heap_array[i]
            i = min_ind

        return deleted_elem


class StructuredElement:
    def __init__(self, data, ind_in, ind_out):
        self.data = data
        self.ind_in = ind_in
        self.ind_out = ind_out

    def __lt__(self, other):
        return self.data < other.data if isinstance(other, StructuredElement) else NotImplemented

    def __gt__(self, other):
        return self.data > other.data if isinstance(other, StructuredElement) else NotImplemented

    def __ge__(self, other):
        return self.data >= other.data if isinstance(other, StructuredElement) else NotImplemented

    def __le__(self, other):
        return self.data <= other.data if isinstance(other, StructuredElement) else NotImplemented

    def unpack(self) -> tuple:
        return self.data, self.ind_in, self.ind_out


def generate_k_arrays(k=10, length=10):
    for num in range(k):
        step = randint(1, 11)
        st = 1
        arr = []
        for _ in range(length):
            st += randint(1, step)  # теперь точно полное возрастание + больше нестабильности
            arr.append(st)
        yield arr


def sort_k_sorted_arrays(arrays: list[list[int]]) -> list[int]:
    result = []
    heap = Heap()
    for i, arr in enumerate(arrays):
        if arr:  # не делаем предположение о том, что у нас все массивы хорошие)
            heap.push_to_heap(StructuredElement(arr[0], 0, i))
    while heap:
        data, ind_in, ind_out = heap.del_from_heap().unpack()  # можем себе такое позволить,
        # потому что в кучу мы сваливаем только объекты типа StructuredElement
        result.append(data)
        if ind_in < len(arrays[ind_out]) - 1:
            heap.push_to_heap(StructuredElement(arrays[ind_out][ind_in + 1], ind_in + 1, ind_out))
    return result


def test_sort_k_sorted_arrays():  # проблема в функции генерации k массивов
    seed(42)  # стабильность
    arrays = list(generate_k_arrays(5, 5))
    flat_sorted = sorted([x for sublist in arrays for x in sublist])
    assert sort_k_sorted_arrays(arrays) == flat_sorted


def test_sort_empty_arrays():
    assert sort_k_sorted_arrays([[], [], []]) == []


def test_sort_single_arrays():
    assert sort_k_sorted_arrays([[1, 2, 3]]) == [1, 2, 3]


def test_sort_different_arrays():
    arrays = [[1, 3], [2], [0, 4, 5]]
    assert sort_k_sorted_arrays(arrays) == [0, 1, 2, 3, 4, 5]
