package ds

// basic data structure, errors are not considered
type Sequence[V any] interface {
	// container
	Build([]V)
	Len() int

	// statice
	Next() V          // return the items one-by-one in sequence order
	GetAt(i int) V    // return the item at index i
	SetAt(i int, x V) // set the item at index i

	// dynamic
	InsertAt(i int, x V) // insert the item at index i
	DeleteAt(i int) V    // delete the item at index i
	InsertFirst(x V)     // insert the item as first item
	DeleteFirst() V      // delete the item at first index
	InsertLast(x V)      // insert the item as last item
	DeleteLast() V       // delete the item at last index
}

// special sequence
type Queue[V any] interface {
	// container
	Build([]V)
	Len() int

	// statice
	Next() V
	GetAt(i int) V
	SetAt(i int, x V)

	// dynamic
	InsertAt(i int, x V)
	DeleteAt(i int) V
	InsertLast(x V)
	DeleteLast() V
}

// special sequence
type Stack[V any] interface {
	// container
	Build([]V)
	Len() int

	// statice
	Next() V
	GetAt(i int) V
	SetAt(i int, x V)

	// dynamic
	InsertAt(i int, x V)
	DeleteAt(i int) V
	InsertLast(x V)
	DeleteLast() V
}
