from binary_node import BinaryNode


class BinaryTree:
    def __init__(self, NodeType=BinaryNode):
        self.root = None
        self.size = 0
        self.NodeType = NodeType

    def __len__(self):
        return self.size

    def __iter__(self):
        if self.root:
            for x in self.root.subtree_iter():
                yield x.item


def build(A):
    tree = BinaryTree()

    # build subtree recursively
    def build_subtree(A, i, j):
        c = (i + j) // 2
        node = tree.NodeType(A[c])
        if i < c:  # need to store more items in left subtree
            node.left = build_subtree(A, i, c - 1)
            node.left.parent = node
        if c < j:  # need to store more items in right subtree
            node.right = build_subtree(A, c + 1, j)
            node.right.parent = node
        return node

    tree.root = build_subtree(A, 0, len(A) - 1)

    return tree


if __name__ == '__main__':
    X = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    tree = build(X)
    it = tree.__iter__()
    print(next(it))
    print(next(it))
    print(next(it))
    print(next(it))
    print(next(it))
