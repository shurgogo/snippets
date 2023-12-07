package ds

import (
	"bytes"
	"fmt"
)

var bits = 32 << (^uint(0) >> 63)

// An IntSet is a set of small non-negative integers.
// Its zero value represents the empty set.
type IntSet struct {
	words []uint
}

// Has reports whether the set contains the non-negative value x.
func (s *IntSet) Has(x int) bool {
	word, bit := x/bits, uint(x%bits)
	return word < len(s.words) && s.words[word]&(1<<bit) != 0
}

// Add adds the non-negative value x to the set.
func (s *IntSet) Add(x int) {
	word, bit := x/bits, uint(x%bits)
	for word >= len(s.words) {
		s.words = append(s.words, 0)
	}
	s.words[word] |= 1 << bit
}

// UnionWith sets s to the union of s and t.
func (s *IntSet) UnionWith(t *IntSet) {
	for i, tword := range t.words {
		if i < len(s.words) {
			s.words[i] |= tword
		} else {
			s.words = append(s.words, tword)
		}
	}
}

// String returns the set as a string of the form "{1 2 3}".
func (s *IntSet) String() string {
	var buf bytes.Buffer
	buf.WriteByte('{')
	for i, word := range s.words {
		if word == 0 {
			continue
		}
		for j := 0; j < bits; j++ {
			if word&(1<<uint(j)) != 0 {
				if buf.Len() > len("{") {
					buf.WriteByte(' ')
				}
				fmt.Fprintf(&buf, "%d", bits*i+j)
			}
		}
	}
	buf.WriteByte('}')
	return buf.String()
}

func (s *IntSet) Len() int {
	return len(s.words)
}

func (s *IntSet) Remove(x int) {
	if s.Has(x) {
		s.words[x/bits] ^= 1 << uint(x%bits)
	}
}

func (s *IntSet) Clear() {
	s.words = make([]uint, 0)
}

func (s *IntSet) Copy() *IntSet {
	x := &IntSet{words: make([]uint, s.Len())}
	copy(x.words, s.words)
	return x
}

func (s *IntSet) AddAll(xs ...int) {
	for _, x := range xs {
		s.Add(x)
	}
}

func (s *IntSet) IntersectWith(t *IntSet) {
	for i := 0; i < min(s.Len(), t.Len()); i++ {
		s.words[i] &= t.words[i]
	}
}
func (s *IntSet) DifferenceWith(t *IntSet) {
	for i := 0; i < s.Len(); i++ {
		s.words[i] ^= s.words[i] & t.words[i]
	}

}
func (s *IntSet) SymmetricDifference(t *IntSet) {
	for i := 0; i < max(s.Len(), t.Len()); i++ {
		if s.Len() <= i {
			s.words = append(s.words, 0)
		}
		s.words[i] ^= t.words[i]
	}
}
func (s *IntSet) Elems() []int {
	elems := make([]int, 0)
	for i, word := range s.words {
		for j := 0; j < bits; j++ {
			if word&(1<<uint(j)) != 0 {
				elems = append(elems, i*bits+j)
			}
		}
	}
	return elems
}
