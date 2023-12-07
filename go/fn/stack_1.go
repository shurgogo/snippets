package main

import (
	"fmt"
	"os"
	"runtime"
)

// 打印调用堆栈信息
func printStack() {
	var buf [4096]byte
	n := runtime.Stack(buf[:], false)
	os.Stdout.Write(buf[:n])
}

func f(n int) {
	fmt.Printf("f(%d)\n", n+0/n)
	defer fmt.Printf("defer %d\n", n)
	f(n - 1)
}

func main() {
	defer printStack()
	f(3)
}
