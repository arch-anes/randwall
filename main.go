package main

import (
	"log/slog"
	"os"
	"time"

	"github.com/arch-anes/randwall/internal/cleanup"
	"github.com/arch-anes/randwall/internal/config"
	"github.com/arch-anes/randwall/internal/connection"
	"github.com/arch-anes/randwall/internal/wallpaper"
)

func main() {
	slog.SetDefault(slog.New(slog.NewTextHandler(os.Stdout, nil)))
	cfg := config.Load()
	cleanupQueue := cleanup.New(cfg)

	for {
		connection.WaitForConnection()
		if path := wallpaper.SetRandom(cfg); path != "" {
			cleanupQueue.Enqueue(path)
		}
		time.Sleep(time.Duration(cfg.Interval) * time.Second)
	}
}
