package ds

// basic data structure, errors are not considered
type Set[K comparable, V any] interface {
	// container
	Build(V)
	Len() int

	// statice
	Find(K)

	// dynamic
	Insert(K, V) // add V to Set with key K
	Delete(K)    // remove K from Set

	// order
	IterOrder() []V // iterate over Set
	FindMin() V     // find minimum key item in Set
	FindMax() V     // find maximum key item in Set
	FindNext(K) V   // find next key item in Set
	FindPrev(K) V   // find prev key item in Set
}

// set without the order operation
type Dictionary[K any, V any] interface {
	// container
	Build(V)
	Len() int

	// statice
	Find(K)

	// dynamic
	Insert(K, V) // add V to Set with key K
	Delete(K)    // remove K from Set

	// order
	FindMin() V   // find minimum key item in Set
	FindMax() V   // find maximum key item in Set
	FindNext(K) V // find next key item in Set
	FindPrev(K) V // find prev key item in Set
}
