package main

// 用channel来实现waitGroup的效果
func watingChannel(works []int) {
	wc := make(chan struct{})
	for _, work := range works {
		go func(work int) {
			defer func() { wc <- struct{}{} }()
			// do something with work
		}(work)
	}

	for range works {
		<-wc
	}
}
