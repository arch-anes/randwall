package connection

import (
	"log/slog"
	"net/http"
	"time"
)

func isConnected() bool {
	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Get("https://1.1.1.1")
	if err != nil {
		slog.Warn("failed to connect to the internet")
		return false
	}
	resp.Body.Close()
	return true
}

func WaitForConnection() {
	for !isConnected() {
		time.Sleep(time.Second)
	}
}
