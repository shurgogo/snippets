package main

import (
	"log"
	"time"
)

// defer trace 可以用来统计函数执行时间
func bigSlowOperation() {
	defer trace("bigSlowOperation")() // don't forget the     extra parentheses
	// ...lots of work...
	time.Sleep(10 * time.Second) // simulate slow operation by sleeping
}
func trace(msg string) func() {
	start := time.Now()
	log.Printf("enter %s", msg)
	return func() {
		log.Printf("exit %s (%s)", msg, time.Since(start))
	}
}
