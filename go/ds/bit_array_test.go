package ds

import (
	"reflect"
	"testing"
)

func TestIntSet_Has(t *testing.T) {
	is := &IntSet{}
	is.AddAll(1, 2, 3)
	testCases := []struct {
		desc   string
		input  int
		output bool
	}{
		{
			desc:   "has 1",
			input:  1,
			output: true,
		},
		{
			desc:   "not has 0",
			input:  0,
			output: false,
		},
	}
	for _, tC := range testCases {
		t.Run(tC.desc, func(t *testing.T) {
			result := is.Has(tC.input)
			if result != tC.output {
				t.Errorf("expected %v, got %v", tC.output, result)
			}
		})
	}
}
func TestIntSet_String(t *testing.T) {
	is := &IntSet{}
	is.AddAll(1, 2, 3)
	testCases := []struct {
		desc   string
		output string
	}{
		{
			desc:   "print {1 2 3}",
			output: "{1 2 3}",
		},
	}
	for _, tC := range testCases {
		t.Run(tC.desc, func(t *testing.T) {
			result := is.String()
			if result != tC.output {
				t.Errorf("expected %v, got %v", tC.output, result)
			}
		})
	}
}
func TestIntSet_Remove(t *testing.T) {
	is := &IntSet{}
	is.AddAll(1, 2, 3)
	testCases := []struct {
		desc   string
		input  int
		output string
	}{
		{
			desc:   "remove 3",
			input:  3,
			output: "{1 2}",
		},
		{
			desc:   "remove 0",
			input:  0,
			output: "{1 2}",
		},
	}
	for _, tC := range testCases {
		t.Run(tC.desc, func(t *testing.T) {
			is.Remove(tC.input)
			result := is.String()
			if result != tC.output {
				t.Errorf("expected %v, got %v", tC.output, result)
			}
		})
	}
}
func TestIntSet_Copy(t *testing.T) {
	is := &IntSet{}
	is.AddAll(1, 2, 3)
	testCases := []struct {
		desc   string
		output string
	}{
		{
			desc:   "copy",
			output: "{1 2 3}",
		},
	}
	for _, tC := range testCases {
		t.Run(tC.desc, func(t *testing.T) {
			s2 := is.Copy()
			result := s2.String()
			if result != tC.output {
				t.Errorf("expected %v, got %v", tC.output, result)
			}
		})
	}
}
func TestIntSet_Clear(t *testing.T) {
	is := &IntSet{}
	is.AddAll(1, 2, 3)
	testCases := []struct {
		desc   string
		output string
	}{
		{
			desc:   "clear",
			output: "{}",
		},
	}
	for _, tC := range testCases {
		t.Run(tC.desc, func(t *testing.T) {
			is.Clear()
			result := is.String()
			if result != tC.output {
				t.Errorf("expected %v, got %v", tC.output, result)
			}
		})
	}
}
func TestIntSet_UnionWith(t *testing.T) {
	testCases := []struct {
		desc   string
		u1     []int
		u2     []int
		output string
	}{
		{
			desc:   "union set {1,2,3} with set {1,2,4}",
			u1:     []int{1, 2, 3},
			u2:     []int{1, 2, 4},
			output: "{1 2 3 4}",
		},
		{
			desc:   "union set {} with set {1,2,4}",
			u1:     []int{},
			u2:     []int{1, 2, 4},
			output: "{1 2 4}",
		},
		{
			desc:   "union set {5,6} with set {1,2,4}",
			u1:     []int{5, 6},
			u2:     []int{1, 2, 4},
			output: "{1 2 4 5 6}",
		},
	}
	for _, tC := range testCases {
		t.Run(tC.desc, func(t *testing.T) {
			s1 := &IntSet{}
			s1.AddAll(tC.u1...)
			s2 := &IntSet{}
			s2.AddAll(tC.u2...)
			s1.UnionWith(s2)
			result := s1.String()
			if result != tC.output {
				t.Errorf("expected %v, got %v", tC.output, result)
			}
		})
	}
}
func TestIntSet_IntersectWith(t *testing.T) {
	testCases := []struct {
		desc   string
		u1     []int
		u2     []int
		output string
	}{
		{
			desc:   "intersect set {1,2,3} with set {1,2,4}",
			u1:     []int{1, 2, 3},
			u2:     []int{1, 2, 4},
			output: "{1 2}",
		},
		{
			desc:   "intersect set {} with set {1,2,4}",
			u1:     []int{},
			u2:     []int{1, 2, 4},
			output: "{}",
		},
		{
			desc:   "intersect set {5,6} with set {1,2,4}",
			u1:     []int{5, 6},
			u2:     []int{1, 2, 4},
			output: "{}",
		},
	}
	for _, tC := range testCases {
		t.Run(tC.desc, func(t *testing.T) {
			s1 := &IntSet{}
			s1.AddAll(tC.u1...)
			s2 := &IntSet{}
			s2.AddAll(tC.u2...)
			s1.IntersectWith(s2)
			result := s1.String()
			if result != tC.output {
				t.Errorf("expected %v, got %v", tC.output, result)
			}
		})
	}
}
func TestIntSet_DifferenceWith(t *testing.T) {
	testCases := []struct {
		desc   string
		u1     []int
		u2     []int
		output string
	}{
		{
			desc:   "difference set {1,2,3} with set {1,2,4}",
			u1:     []int{1, 2, 3},
			u2:     []int{1, 2, 4},
			output: "{3}",
		},
		{
			desc:   "difference set {} with set {1,2,4}",
			u1:     []int{},
			u2:     []int{1, 2, 4},
			output: "{}",
		},
		{
			desc:   "difference set {5,6} with set {1,2,4}",
			u1:     []int{5, 6},
			u2:     []int{1, 2, 4},
			output: "{5 6}",
		},
	}
	for _, tC := range testCases {
		t.Run(tC.desc, func(t *testing.T) {
			s1 := &IntSet{}
			s1.AddAll(tC.u1...)
			s2 := &IntSet{}
			s2.AddAll(tC.u2...)
			s1.DifferenceWith(s2)
			result := s1.String()
			if result != tC.output {
				t.Errorf("expected %v, got %v", tC.output, result)
			}
		})
	}
}
func TestIntSet_SymmetricDifference(t *testing.T) {
	testCases := []struct {
		desc   string
		u1     []int
		u2     []int
		output string
	}{
		{
			desc:   "symmetric difference set {1,2,3} with set {1,2,4}",
			u1:     []int{1, 2, 3},
			u2:     []int{1, 2, 4},
			output: "{3 4}",
		},
		{
			desc:   "symmetric difference set {} with set {1,2,4}",
			u1:     []int{},
			u2:     []int{1, 2, 4},
			output: "{1 2 4}",
		},
		{
			desc:   "symmetric difference set {5,6} with set {1,2,4}",
			u1:     []int{5, 6},
			u2:     []int{1, 2, 4},
			output: "{1 2 4 5 6}",
		},
	}
	for _, tC := range testCases {
		t.Run(tC.desc, func(t *testing.T) {
			s1 := &IntSet{}
			s1.AddAll(tC.u1...)
			s2 := &IntSet{}
			s2.AddAll(tC.u2...)
			s1.SymmetricDifference(s2)
			result := s1.String()
			if result != tC.output {
				t.Errorf("expected %v, got %v", tC.output, result)
			}
		})
	}
}
func TestIntSet_Elems(t *testing.T) {
	testCases := []struct {
		desc   string
		input  []int
		output []int
	}{
		{
			desc:   "set {1,2,3}",
			input:  []int{1, 2, 3},
			output: []int{1, 2, 3},
		},
		{
			desc:   "set {}",
			input:  []int{},
			output: []int{},
		},
	}
	for _, tC := range testCases {
		t.Run(tC.desc, func(t *testing.T) {
			s1 := &IntSet{}
			s1.AddAll(tC.input...)
			result := s1.Elems()
			if !reflect.DeepEqual(result, tC.output) {
				t.Errorf("expected %v, got %v", tC.output, result)
			}
		})
	}
}
