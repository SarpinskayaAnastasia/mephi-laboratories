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
        self.height = 0  # по умолчанию лист


def update_height(node: Node):
    left_height = node.left.height if node.left else -1
    right_height = node.right.height if node.right else -1
    node.height = 1 + max(left_height, right_height)


def push(new: Node, root: Node):
    if not root:
        return new
    if new.val >= root.val:
        root.right = push(new, root.right)
    else:
        root.left = push(new, root.left)
    # Мы прописываем перерасчет только здесь, потому что мы после сравнений не выходим из функции,
    # а продолжаем ее работу
    root.height = 1 + max(root.left.height if root.left else -1, root.right.height if root.right else -1)
    return root


def pop(val: int, root: Node) -> Node or None:
    if not root:
        return None  # мы дошли до конца и не нашли интересующий нас узел.
        # А None мы записываем в потомки родителя, у которого этот конкретный потомок уже был None

    if val < root.val:
        root.left = pop(val, root.left)
    elif val > root.val:
        root.right = pop(val, root.right)
    else:  # НАШЛИ ЗНАЧЕНИЕ! УРААА
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
        # Эти две штуки подходят и для случая с 1 потомком, и для листов. Почему?
        # Когда мы не имеем потомков, мы возвращаем None. И этот None мы записываем в потомки родителя.
        # Таким образом мы легко и просто стираем лист.
        mln = root.right
        while mln.left:
            mln = mln.left
        root.val = mln.val
        root.right = pop(mln.val, root.right)
    root.height = 1 + max(root.left.height if root.left else -1, root.right.height if root.right else -1)
    return root


def find(val: int, root: Node) -> bool:
    if root is None:
        return False
    if val == root.val:
        return True
    elif val < root.val:
        return find(val, root.left)
    else:
        return find(val, root.right)


class BST:
    def __init__(self):
        self.root = None
        self.av_depth = 0
        self.max_depth = 0
        self._total_leaf_depth = 0
        self._leaf_count = 0

    @staticmethod
    def is_root(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> R:
            if self.root is None:
                raise IndexError("tree doesn't exist (root is None)")
            return func(self, *args, **kwargs)

        return wrapper

    def pu(self, new_node: Node):
        if not self.root:
            self.root = new_node
        else:
            self.root = push(new_node, self.root)

    @is_root
    def po(self, val: int):
        self.root = pop(val, self.root)

    @is_root
    def fi(self, value: int) -> bool:
        return find(value, self.root)

    def _calc_depths(self, node, current_depth):
        if not node:
            return

        if not node.height:
            self._total_leaf_depth += current_depth
            self._leaf_count += 1

        self._calc_depths(node.left, current_depth + 1)
        self._calc_depths(node.right, current_depth + 1)

    @is_root
    def calculate_depths(self):
        self.max_depth = self.root.height + 1
        self._calc_depths(self.root, 1)

        try:
            self.av_depth = self._total_leaf_depth / self._leaf_count
        except ZeroDivisionError:
            self.av_depth = 0


class AVL(BST):
    @staticmethod
    def is_root(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> R:
            if self.root is None:
                raise IndexError("tree doesn't exist (root is None)")
            return func(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def get_balance(node: Node) -> int:
        if not node:
            return 0
        height_l = node.left.height if node.left else 0
        height_r = node.right.height if node.right else 0
        return height_l - height_r

    @staticmethod
    def _rotate_left(z: Node) -> Node:
        y = z.right
        t2 = y.left
        y.left = z
        z.right = t2

        update_height(z)
        update_height(y)
        return y

    @staticmethod
    def _rotate_right(z: Node) -> Node:
        y = z.left
        t3 = y.right
        y.right = z
        z.left = t3

        update_height(z)
        update_height(y)
        return y

    def _rebalance(self, node: Node) -> Node:
        if not node:
            return node

        node.left = self._rebalance(node.left)
        node.right = self._rebalance(node.right)

        update_height(node)
        balance = self.get_balance(node)

        if balance > 1:
            if self.get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1:
            if self.get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

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

    @is_root
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
