from binary_search_tree_node import BSTNode
from binary_tree import BinaryTree


class SetBinaryTree(BinaryTree):  # aka Binary Search Tree
    def __init__(self):
        super().__init__(BSTNode)

    def iter_order(self):
        yield from self

    def build(self, X):
        for x in X:
            self.insert(x)

    def find_min(self):
        if self.root:
            return self.root.subtree_first().item

    def find_max(self):
        if self.root:
            return self.root.subtree_last().item

    def find(self, k):
        if self.root:
            node = self.root.subtree_find(k)
            if node:
                return node.item

    def find_next(self, k):
        if self.root:
            node = self.root.subtree_find_next(k)
            if node:
                return node.item

    def find_prev(self, k):
        if self.root:
            node = self.root.subtree_find_prev(k)
            if node:
                return node.item

    def insert(self, x):
        new_node = self.NodeType(x)
        if self.root:
            self.root.subtree_insert(new_node)
            if new_node.parent is None:
                return False
        else:
            self.root = new_node
        self.size += 1
        return True

    def delete(self, k):
        assert self.root
        node = self.root.subtree_find(k)
        assert node
        ex = node.subtree_delete()
        if ex.parent is None:
            self.root = None
        self.size -= 1
        return ex.item
