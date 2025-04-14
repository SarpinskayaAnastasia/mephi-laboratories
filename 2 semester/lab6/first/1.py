from linked_list import OnceNode


class Solution:
    def split_list(self, head):
        # Метод "бегунков" (slow и fast) для разделения списка пополам
        slow = head
        fast = head.next

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        right = slow.next  # Начало правой части
        slow.next = None  # Разрываем связь между левой и правой частями

        return head, right  # left = head, right = slow.next

    def merge(self, left, right):
        # Фиктивный узел для упрощения кода
        dummy = OnceNode(0)
        tail = dummy

        while left and right:
            if left < right:
                tail.next = left
                left = left.next
            else:
                tail.next = right
                right = right.next
            tail = tail.next

        # Присоединяем оставшиеся узлы
        tail.next = left if left else right

        return dummy.next  # Истинное начало списка

    def merge_sort(self, head):
        # Базовый случай: пустой список или один элемент
        if head is None or head.next is None:
            return head

        # Разделение списка на две части
        left, right = self.split_list(head)

        # Рекурсивная сортировка каждой части
        left_sorted = self.merge_sort(left)
        right_sorted = self.merge_sort(right)

        # Слияние двух отсортированных списков
        return self.merge(left_sorted, right_sorted)

    def print_list(self, head):
        while head:
            print(head, end=" -> " if head.next else "\n")
            head = head.next


if __name__ == "__main__":
    sol = Solution()
    # Создаём список вручную (без LinkedList)
    node1 = OnceNode(38)
    node2 = OnceNode(27)
    node3 = OnceNode(43)
    node4 = OnceNode(3)
    node5 = OnceNode(9)
    node6 = OnceNode(82)
    node7 = OnceNode(10)

    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node5
    node5.next = node6
    node6.next = node7

    print("Исходный список:")
    sol.print_list(node1)

    sorted_head = sol.merge_sort(node1)
    print("\nОтсортированный список:")
    sol.print_list(sorted_head)
