package main

import "testing"

func addOneNormal(i int) {
	i = i + 1
}
func addOneAnd(i int) {
	i += i & -i
}

func BenchmarkAddOneNormal(b *testing.B) {
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		addOneNormal(i)
	}
}

func BenchmarkAddOneAnd(b *testing.B) {
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		addOneAnd(i)
	}
}
