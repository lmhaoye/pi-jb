package main

import (
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"strings"
)

func getIP() string {
	resp, err := http.Get("http://ipinfo.io/ip")
	if err != nil {
		return ""
	}
	defer resp.Body.Close()
	content, _ := ioutil.ReadAll(resp.Body)
	return string(content)
}

func GetPulicIP() string {
	conn, _ := net.Dial("udp", "8.8.8.8:80")
	defer conn.Close()
	localAddr := conn.LocalAddr().String()
	idx := strings.LastIndex(localAddr, ":")
	return localAddr[0:idx]
}
func main() {
	fmt.Println("Hello World")
	fmt.Println(getIP())
	fmt.Println(GetPulicIP())
}
