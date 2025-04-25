from linked_list import OnceNode, LinkedList


class Solution:
    @staticmethod
    def split_list(head: OnceNode) -> tuple[OnceNode, OnceNode]:
        slow = head
        fast = head.next

        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

        right = slow.next
        slow.next = None

        return head, right  # left = head, right = slow.next

    @staticmethod
    def merge(left: OnceNode, right: OnceNode) -> OnceNode:
        dummy = OnceNode(None)
        pseudo_head = dummy

        while left and right:
            if left < right:
                pseudo_head.next = left
                left = left.next
            else:
                pseudo_head.next = right
                right = right.next
            pseudo_head = pseudo_head.next

        pseudo_head.next = left if left else right

        return dummy.next

    def merge_sort(self, head: OnceNode) -> OnceNode or None:
        if head is None or head.next is None:
            return head

        left, right = self.split_list(head)

        left_sorted = self.merge_sort(left)
        right_sorted = self.merge_sort(right)

        return self.merge(left_sorted, right_sorted)

    @staticmethod
    def print_list(head: OnceNode):
        while head:
            print(head, end=" -> " if head.next else "\n")
            head = head.next


if __name__ == "__main__":
    sol = Solution()
    linked_list = LinkedList()
    linked_list.append(38)
    linked_list.append(27)
    linked_list.append(43)
    linked_list.append(3)
    linked_list.append(9)
    linked_list.append(82)
    linked_list.append(10)
    print("Исходный список:")
    sol.print_list(linked_list.head)

    sorted_head = sol.merge_sort(linked_list.head)
    print("\nОтсортированный список:")
    sol.print_list(sorted_head)
