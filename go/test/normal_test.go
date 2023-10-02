package main

import "testing"

func TestNormal(t *testing.T) {
	cases := []struct {
		input, output int
		msg           string
	}{
		{
			input:  1,
			output: 1,
			msg:    "hello",
		},
	}

	for _, c := range cases {
		result := Normal(c.input)
		if result != c.output {
			t.Errorf("got %v, want %v", result, c.output)
		}
	}
}
