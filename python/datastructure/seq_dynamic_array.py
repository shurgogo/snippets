from seq_array import SeqArray


class SeqDynamicArray(SeqArray):
    def __init__(self, r=2):  # O(1)
        super().__init__()
        self.size = 0
        self.r = r
        self._compute_bounds()
        self._resize(0)

    def __len__(self):  # O(1)
        return self.size

    def __iter__(self):  # O(n)
        for i in range(len(self)):
            yield self.A[i]

    def build(self, X):  # O(n)
        for x in X:
            self.insert_last(x)

    def _compute_bounds(self):
        self.upper = len(self.A)
        self.lower = len(self.A) // (self.r * self.r)

    def _resize(self, n):
        if (self.lower < n < self.upper):
            return
        m = max(n, 1) * self.r
        A = [None] * m
        self._copy_foward(0, self.size, A, 0)
        self.A = A
        self._compute_bounds()

    def insert_last(self, x):
        self._resize(self.size + 1)
        self.A[self.size] = x
        self.size += 1
