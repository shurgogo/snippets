class BinaryNode:
    def __init__(self, x):  # O(1)
        self.item = x
        self.left = None
        self.right = None
        self.parent = None
        self.subtree_update()

    def subtree_update(self):
        pass

    def maintain(self):
        pass

    def subtree_iter(self):  # O(n)
        if self.left:
            yield from self.left.subtree_iter()
        yield self
        if self.right:
            yield from self.right.subtree_iter()

    def subtree_first(self):  # O(h), h means height
        if self.left:
            return self.left.subtree_first()
        else:
            return self

    def subtree_last(self):  # O(h)
        if self.right:
            return self.right.subtree_last()
        else:
            return self

    def successor(self):  # O(h)
        if self.right:
            return self.right.subtree_first()
        while self.parent and self is self.parent.left:
            self = self.parent
        return self.parent

    def predecessor(self):  # O(h)
        if self.left:
            return self.left.subtree_last()
        while self.parent and self is self.parent.left:
            self = self.parent
        return self.parent

    def subtree_insert_before(self, x):  # O(h)
        if self.left:
            self = self.left.subtree_last()
            self.right, x.parent = x, self
        else:
            self.left, x.parent = x, self
        self.maintain()

    def subtree_insert_after(self, x):  # O(h)
        if self.right:
            self = self.right.subtree_first()
            self.left, x.parent = x, self
        else:
            self.right, x.parent = x, self
        self.maintain()

    def subtree_delete(self):  # O(h)
        if self.left or self.right:
            if self.left:
                x = self.predecessor()
            else:
                x = self.successor()
            self.item, x.item = x.item, self.item
            return x.subtree_delete()
        if self.parent:
            if self is self.parent.left:
                self.parent.left = None
            else:
                self.parent.right = None
            self.parent.maintain()
        return self


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
