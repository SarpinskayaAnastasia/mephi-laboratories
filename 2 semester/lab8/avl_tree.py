import functools
from random import randint
from typing import Callable, TypeVar, ParamSpec
import time
from sys import setrecursionlimit

setrecursionlimit(1200)  # у нас максимум 1000 элементов, но берем с запасом

P = ParamSpec("P")
R = TypeVar("R")


class Node:
    def __init__(self, content):
        self.val = content
        self.left = None
        self.right = None


def push(new: Node, root: Node):
    if not root:
        return new
    if new.val >= root.val:
        root.right = push(new, root.right)
    else:
        root.left = push(new, root.left)
    return root


def pop(val: int, node: Node) -> Node or None:
    if not Node:
        return None  # не нашли интересующий нас узел

    if val < node.val:
        node.left = pop(val, node.left)
    elif val > node.val:
        node.right = pop(val, node.right)
    else:
        if not node.left:
            return node.right
        elif not node.right:
            return node.left
        mln = node.right
        while mln.left:
            mln = mln.left
        node.val = mln.val
        node.right = pop(mln.val, node.right)
    return node


class BST:
    def __init__(self):
        self.root = None
        self.av_depth = 0
        self.max_depth = 0
        self._total_leaf_depth = 0
        self._leaf_count = 0

    def pu(self, new_node: Node):
        if not self.root:
            self.root = new_node
        else:
            self.root = push(new_node, self.root)

    def po(self, val: int):
        self.root = pop(val, self.root)

    def find(self, value: int, node: Node = None) -> bool:
        if node is None:
            node = self.root
        if node is None:
            return False
        if value == node.val:
            return True
        elif value < node.val:
            return self.find(value, node.left)
        else:
            return self.find(value, node.right)

    def _calc_depths(self, node, current_depth):
        if not node:
            return

        self.max_depth = max(self.max_depth, current_depth)

        if not (node.left or node.right):
            self._total_leaf_depth += current_depth
            self._leaf_count += 1

        self._calc_depths(node.left, current_depth + 1)
        self._calc_depths(node.right, current_depth + 1)

    def calculate_depths(self):
        self.max_depth = 0
        self._calc_depths(self.root, 1)

        if self._leaf_count > 0:
            self.av_depth = self._total_leaf_depth / self._leaf_count
        else:
            self.av_depth = 0


class AVL(BST):
    def height(self, node: Node) -> int:
        if not node:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def get_balance(self, node: Node) -> int:
        return self.height(node.left) - self.height(node.right) if node else 0

    @staticmethod
    def rotate_left(z: Node) -> Node:
        y = z.right
        t2 = y.left
        y.left = z
        z.right = t2
        return y

    @staticmethod
    def rotate_right(z: Node) -> Node:
        y = z.left
        t3 = y.right
        y.right = z
        z.left = t3
        return y

    def _rebalance(self, node: Node) -> Node:
        if not node:
            return node

        node.left = self._rebalance(node.left)
        node.right = self._rebalance(node.right)

        balance = self.get_balance(node)

        if balance > 1:
            if self.get_balance(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1:
            if self.get_balance(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    @staticmethod
    def avlize(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> R:
            result = func(self, *args, **kwargs)
            self.root = self._rebalance(self.root)
            return result

        return wrapper

    @avlize
    def pu(self, new_node: Node):
        super().pu(new_node)

    @avlize
    def po(self, val: int):
        super().po(val)


def gen_random(lot: int = 1000):
    while lot:
        yield randint(1, 1001)
        lot -= 1


def gen_sorted(lot: int = 1000):
    step = 10
    start = 1
    while lot:
        yield randint(start, start + step)
        start += step
        lot -= 1


def gen_pattern(lot: int = 1000):
    yield 1
    for i in range(2, lot + 1):
        yield i + (-1) ** (i & 1)


def benchmark(tree_class, array):
    tree = tree_class()
    start = time.time()
    for v in array:
        tree.pu(Node(v))
    print_tree(tree.root)
    print('------------------------')
    elapsed = time.time() - start
    tree.calculate_depths()
    return elapsed, tree.av_depth, tree.max_depth


def print_tree(node, prefix="", is_left=True, max_depth=5, depth=0):
    """Красивый вывод бинарного дерева в консоль."""
    if node is None or depth >= max_depth:
        return
    print_tree(node.right, prefix + ("│   " if is_left else "    "), False, max_depth, depth + 1)
    print(prefix + ("└── " if is_left else "┌── ") + str(node.val))
    print_tree(node.left, prefix + ("    " if is_left else "│   "), True, max_depth, depth + 1)


def main():
    datasets = {
        "random": list(gen_random()),
        "sorted": list(gen_sorted()),
        "pattern": list(gen_pattern()),
    }

    for name, data in datasets.items():
        print(f"\n{name.upper()} DATASET:")

        bst_result = benchmark(BST, data)
        avl_result = benchmark(AVL, data)

        print(f"BST: time = {bst_result[0]:.4f}s, avg depth = {bst_result[1]:.2f}, max depth = {bst_result[2]}")
        print(f"AVL: time = {avl_result[0]:.4f}s, avg depth = {avl_result[1]:.2f}, max depth = {avl_result[2]}")


if __name__ == "__main__":
    main()
