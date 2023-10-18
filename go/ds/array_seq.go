package ds

type Array[V any] struct {
	c     int // current index
	size  int
	items []V
}

func (a *Array[V]) Build(items []V) {
	a.items = make([]V, len(items))
	copy(a.items, items)
	a.size = len(a.items)
}

func (a *Array[V]) Len() int { return len(a.items) }

func (a *Array[V]) Next() V {
	a.c += 1
	return a.items[a.c-1]
}

func (a *Array[V]) GetAt(i int) V { return a.items[i] }

func (a *Array[V]) SetAt(i int, x V) { a.items[i] = x }

func (a *Array[V]) InsertAt(i int, x V) {
	newItems := make([]V, len(a.items)+1)
	copy(newItems[:i], a.items[:i])
	newItems[i] = x
	copy(newItems[i+1:], a.items[i:])
	a.Build(newItems)
}

func (a *Array[V]) DeleteAt(i int) V {
	newItems := make([]V, len(a.items)-1)
	copy(newItems[:i], a.items[:i])
	v := a.items[i]
	copy(newItems[i:], a.items[i+1:])
	a.Build(newItems)
	return v
}

func (a *Array[V]) InsertFirst(x V) {
	a.InsertAt(0, x)
}

func (a *Array[V]) DeleteFirst() V {
	return a.DeleteAt(0)
}

func (a *Array[V]) InsertLast(x V) {
	a.InsertAt(a.Len(), x)
}

func (a *Array[V]) DeleteLast() V {
	return a.DeleteAt(a.Len() - 1)
}
