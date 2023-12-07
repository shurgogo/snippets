package main

import (
	"fmt"
	"os"
	"runtime"
)

func traceStack(skip int) {
	pc, file, line, ok := runtime.Caller(skip)
	if !ok {
		fmt.Printf("runtime.Caller(%d) failed", skip)
		os.Exit(1)
	}
	fmt.Printf("func name is %s\nfile name is %s\nline number is %d\n",
		runtime.FuncForPC(pc).Name(), file, line)
}

func main() {
	traceStack(0)
}
