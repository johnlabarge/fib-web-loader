package main

import (
	"fmt"
	"net/http"
	"os"
	"strconv"
	"time"
)


func fib(n int) int {
//	fmt.Println("Calculating fib " +  strconv.Itoa(n))
	if n > 1 {
		return fib(n-1) + fib(n-2)
	}
	return 1
}
func recordRequest(requestInfo string) {
	host := os.Getenv("HOST")
	fmt.Println("host:" + host + ":" + requestInfo)
}
func handler(w http.ResponseWriter, r *http.Request) {
	jobId := time.Now().UnixNano()
	recordRequest(r.URL.Path)
	nS := r.URL.Path[1:]
	var n, err = strconv.Atoi(nS)
	if err != nil {
		n = 0
	}
	go func() {
		result := fib(n)
		fmt.Printf("RESULT for job %d is %d", jobId, result)
	}()
	fmt.Fprintf(w, "{\n\tjob:%d,", jobId)
	fmt.Fprintf(w, "\n\tnumber:%d,\n\tfibonucci:?\n}", n)
}

func main() {
	http.HandleFunc("/", handler)
	http.ListenAndServe(":8080", nil)
}
