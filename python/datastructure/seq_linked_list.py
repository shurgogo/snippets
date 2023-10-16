class LinkedListNode:
    def __init__(self, x):
        self.item = x
        self.next = None

    def later_node(self, i):
        if i == 0:
            return self
        assert self.next
        return self.next.later_node(i - 1)


class SeqLinkedList:
    def __init__(self, head: LinkedListNode):  # O(1)
        self.head = head
        self.size = 0

    def __len__(self):  # O(1)
        return self.size

    def __iter__(self):  # O(n) iter_seq
        node = self.head
        while node:
            yield node.item
            node = node.next

    def build(self, X):  # O(n)
        for x in reversed(X):
            self.insert_firts(x)

    def get_at(self, i):  # O(n)
        node = self.head.later_node(i)
        return node.item

    def set_at(self, i, x):  # O(n)
        node = self.head.later_node(i)
        node.item = x

    def insert_first(self, x):  # O(1)
        new_node = LinkedListNode(x)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def delete_first(self):  # O(1)
        x = self.head
        self.head = self.head.next
        self.size -= 1
        return x

    def insert_at(self, i, x):
        if i == 0:
            self.insert_first(x)
            return
        new_node = LinkedListNode(x)
        node = self.head.later_node(i - 1)
        new_node.next = node.next
        node.next = new_node
        self.size += 1

    def delete_at(self, i):
        if i == 0:
            self.delete_first()
            return
        node = self.head.later_node(i - 1)
        x = node.next.item
        node.next = x.next
        self.size -= 1
        return x

    def insert_last(self, x):  # O(n)
        self.insert_at(len(self), x)

    def delete_last(self):  # O(n)
        return self.delete_at(len(self) - 1)
