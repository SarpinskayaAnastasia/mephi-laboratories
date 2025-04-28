class TreeNode:
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None


def dfs(node: TreeNode) -> tuple[dict, dict]:
    parent_map = {}
    depth_map = {}

    def _dfs(current: TreeNode, parent: TreeNode or None, depth: int):
        if current is None:
            return
        parent_map[current] = parent
        depth_map[current] = depth
        _dfs(current.left, current, depth + 1)
        _dfs(current.right, current, depth + 1)

    _dfs(node, None, 0)
    return parent_map, depth_map


def mirrorize(node: TreeNode):
    if node is None:
        return
    temp = node.left
    node.left = node.right
    node.right = temp

    mirrorize(node.left)
    mirrorize(node.right)


class BinaryTree:
    def __init__(self):
        self.head = None
        self.parent = {}
        self.depth = {}

    def lca(self, u: TreeNode, v: TreeNode) -> TreeNode or None:
        # обработка исключений
        if not self.head:
            return
        if not self.parent or not self.depth:
            self.parent, self.depth = dfs(self.head)
        if u not in self.depth or v not in self.depth:
            return

        # сам рекурсивный алгоритм
        if u is v:
            return u
        elif self.depth[u] > self.depth[v]:
            return self.lca(self.parent[u], v)
        elif self.depth[u] < self.depth[v]:
            return self.lca(u, self.parent[v])
        return self.lca(self.parent[u], self.parent[v])  # вот мы добрались до одного уровня и поднимаемся до родителя.

    def mirror(self):
        mirrorize(self.head)
        # self.depth = self.parent = None подумали, что это нужно,
        # но по факту нет, ибо ни родители, ни глубина не меняются

    def distance(self, u: TreeNode, v: TreeNode) -> int or None:
        if not self.head:
            return
        if not self.parent or not self.depth:
            self.parent, self.depth = dfs(self.head)
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]


def print_tree(node, prefix="", is_left=True):
    """Красивый вывод бинарного дерева в консоль."""
    if node is not None:
        print_tree(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.data))
        print_tree(node.left, prefix + ("    " if is_left else "│   "), True)


if __name__ == "__main__":
    '''
    Создаём дерево:
            a
           / \\
          b   c
         / \\
        d   e
    '''
    a = TreeNode("a")
    b = TreeNode("b")
    c = TreeNode("c")
    d = TreeNode("d")
    e = TreeNode("e")

    a.left = b
    a.right = c
    b.left = d
    b.right = e

    tree = BinaryTree()
    tree.head = a
    print_tree(tree.head)

    lca1 = tree.lca(d, e)
    print(f"LCA of {d.data} and {e.data} is: {lca1.data}")  # Ожидается: b

    lca2 = tree.lca(d, c)
    print(f"LCA of {d.data} and {c.data} is: {lca2.data}")  # Ожидается: a

    lca3 = tree.lca(b, d)
    print(f"LCA of {b.data} and {d.data} is: {lca3.data}")  # Ожидается: b

    print(f"Distance between {d.data} and {e.data} is: {tree.distance(d, e)}")  # 2
    print(f"Distance between {d.data} and {c.data} is: {tree.distance(d, c)}")  # 3
    print(f"Distance between {a.data} and {c.data} is: {tree.distance(a, c)}")  # 1

    tree.mirror()
    print_tree(tree.head)

    lca4 = tree.lca(d, e)
    print(f"After mirroring, LCA of {d.data} and {e.data} is: {lca4.data}")  # Должно быть всё ещё b
