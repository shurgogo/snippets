from binary_tree import BinaryTree, BinaryNode


class BSTNode(BinaryNode):
    def subtree_find(self, k):  # O(h)
        if k < self.item.key:  # item stores both key and value
            if self.left:
                return self.left.subtree_find(k)
        elif k > self.item.key:
            if self.right:
                return self.right.subtree_find(k)
        else:
            return self
        return None

    def subtree_find_next(self, k):  # O(h)
        if k >= self.item.key:  # next item of k must in right subtree
            if self.right:
                return self.right.subtree_find_next(k)
            else:
                return None
        elif self.left:  # next item of k must in left subtree
            x = self.left.subtree_find_next(k)
            if x:
                return x
        return self  # next item of k is self

    def subtree_find_prev(self, k):  # O(h)
        if k <= self.item.key:
            if self.left:
                return self.left.subtree_find_prev(k)
            else:
                return None
        elif self.right:
            x = self.right.subtree_find_prev(k)
            if x:
                return x
        return self

    def subtree_insert(self, x):  # O(h)
        if x.item.key < self.item.key:
            if self.left:
                self.left.subtree_insert(x)
            else:
                self.subtree_insert_before(x)  # insert x before self
        elif x.item.key > self.item.key:
            if self.right:
                self.right.subtree_insert(x)
            else:
                self.subtree_insert_after(x)  # insert x after self
        else:
            self.item = x.item


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
