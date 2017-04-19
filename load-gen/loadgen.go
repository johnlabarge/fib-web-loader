package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"
	"sync"
	"time"
)

func convertToInt(s string, def int) int {
	var result, err = strconv.Atoi(s)
	fmt.Println(result)
	if err != nil {
		fmt.Println(err)
		result = def
	}
	return result
}

func doRequest(url string, sleeptime int) {
	timeout := time.Duration(5 * time.Minute)
	client := http.Client{
		Timeout: timeout,
	}
	for true {

		resp, err := client.Get(url)
		if err != nil {
			fmt.Println(err)
		} else {
			defer resp.Body.Close()
			responseData, err := ioutil.ReadAll(resp.Body)
			if err != nil {
				fmt.Println(err)
			} else {
				t := time.Now()
				fmt.Print(t.Format("15:04:05.99999999"))
				fmt.Println(string(responseData))
			}
		}
		time.Sleep(time.Duration(sleeptime) * time.Second)
	}
}
func main() {
	var wg sync.WaitGroup
	fmt.Println("starting requests")
	var url = os.Getenv("URL")
	var num = convertToInt(os.Getenv("NUM"), 40)
	fmt.Println("NUM=" + string(num))
	var threads = convertToInt(os.Getenv("THREADS"), 3)
	var sleeptime = convertToInt(os.Getenv("SLEEPTIME"), 3)
	url += "/" + strconv.Itoa(num)
	wg.Add(threads)
	for i := 0; i < threads; i++ {
		go doRequest(url, sleeptime)
	}
	wg.Wait()
}
