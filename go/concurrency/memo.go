package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"sync"
	"time"
)

type result struct {
	value interface{}
	err   error
}

type request struct {
	key      string
	response chan<- result
}

type entry struct {
	res   result
	ready chan struct{}
}

func (e *entry) call(f Func, key string) {
	e.res.value, e.res.err = f(key)
	close(e.ready)
}

func (e *entry) deliver(resp chan<- result) {
	<-e.ready
	resp <- e.res
}

type Func func(string) (interface{}, error)

type Memo struct {
	requests chan request
}

func (m *Memo) server(f Func) {
	cache := make(map[string]*entry)
	for req := range m.requests {
		e := cache[req.key]
		if e == nil {
			e = &entry{ready: make(chan struct{})}
			cache[req.key] = e
			go e.call(f, req.key)
		}
		go e.deliver(req.response)
	}
}

func New(f Func) *Memo {
	m := &Memo{requests: make(chan request)}
	go m.server(f)
	return m
}

func (m *Memo) Get(key string) (interface{}, error) {
	resp := make(chan result)
	m.requests <- request{key: key, response: resp}
	res := <-resp
	return res.value, res.err
}

func (m *Memo) Close() {
	close(m.requests)
}

func httpGetBody(url string) (interface{}, error) {
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	return io.ReadAll(resp.Body)
}

func incomingURLs() chan string {
	urls := []string{
		"https://golang.org",
		"https://godoc.org",
		"http://play.golang.org",
		"https://golang.org",
		"https://godoc.org",
		"http://play.golang.org",
		"http://gopl.io",
	}
	iu := make(chan string)
	go func() {
		for _, url := range urls {
			iu <- url
		}
	}()
	go func() {
		os.Stdin.Read(make([]byte, 1))
		close(iu)
	}() // 优雅关停
	return iu
}

func main() {
	m := New(httpGetBody)
	var n sync.WaitGroup
	for url := range incomingURLs() {
		n.Add(1)
		go func(url string) {
			start := time.Now()
			value, err := m.Get(url)
			if err != nil {
				log.Print(err)
			}
			fmt.Printf("%s, %s, %d bytes\n", url, time.Since(start), len(value.([]byte)))
			n.Done()
		}(url)
	}
	n.Wait()
	fmt.Println("stopped")
}
