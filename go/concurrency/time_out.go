package main

import (
	//"fmt"
	"net/http"
	_ "net/http/pprof"
	"time"
)

// 当从work收到信息后,函数返回，但
func incorrect(work <-chan struct{}) {
	select {
	case <-time.After(5 * time.Minute):
		//fmt.Println("time out")
	case <-work:
		//fmt.Println("work done")
		return
	}
}

func correct(work <-chan struct{}) {
	ticker := time.NewTicker(5 * time.Minute)
	select {
	case <-ticker.C:
		//fmt.Println("time out")
	case <-work:
		//fmt.Println("work done")
		return
	}
}

func f1(n int) {
	work := make(chan struct{})
	for i := 0; i < n; i++ {
		go incorrect(work)
	}
	time.Sleep(1 * time.Minute)
	work <- struct{}{}
	time.Sleep(10 * time.Minute)
}
func f2(n int) {
	work := make(chan struct{})
	for i := 0; i < n; i++ {
		go correct(work)
	}
	time.Sleep(1 * time.Minute)
	work <- struct{}{}
	time.Sleep(10 * time.Minute)
}

func main() {
	go func() {
		http.ListenAndServe("127.0.0.1:9999", nil)
	}()
	f1(1000)

}
