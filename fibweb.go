package main

import (
	"fmt"
	"net/http"
	"os"
	"strconv"
)

func fib(n int) int {
	if n > 1 {
		return fib(n-1) + fib(n-2)
	}
	return 1
}
func recordRequest() {
	host := os.Getenv("HOST")
	fmt.Println("host:" + host)
}
func handler(w http.ResponseWriter, r *http.Request) {
	recordRequest()
	nS := r.URL.Path[1:]
	var n, err = strconv.Atoi(nS)
	if err != nil {
		n = 0
	}
	fmt.Fprintf(w, "<h1> fib(%d) = %d </h1>", n, fib(n))
}

func main() {
	http.HandleFunc("/", handler)
	http.ListenAndServe(":8080", nil)
}
