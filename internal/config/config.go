package config

import (
	"encoding/json"
	"log/slog"
	"os"
	"path/filepath"

	"github.com/fsnotify/fsnotify"
)

type Config struct {
	APIKey        string          `json:"api_key"`
	MaxPage       int             `json:"max_page"`
	Categories    map[string]bool `json:"categories"`
	Purity        map[string]bool `json:"purity"`
	Tags          string          `json:"tags"`
	Interval      int             `json:"interval"`
	Keep          int             `json:"keep"`
	MinResolution string          `json:"min_resolution"`
	Sorting       string          `json:"sorting"`
	path          string
}

func defaultConfig() *Config {
	return &Config{
		APIKey:  "",
		MaxPage: 10,
		Categories: map[string]bool{
			"general": true,
			"anime":   true,
			"people":  true,
		},
		Purity: map[string]bool{
			"sfw":     true,
			"sketchy": false,
			"nsfw":    false,
		},
		Tags:          "-microsoft -logo +trees",
		Interval:      30,
		Keep:          10,
		MinResolution: "1920x1080",
		Sorting:       "toplist",
	}
}

func configDir() string {
	if dir := os.Getenv("XDG_CONFIG_HOME"); dir != "" {
		return filepath.Join(dir, "randwall")
	}
	home, err := os.UserHomeDir()
	if err != nil {
		slog.Error("error getting home directory", "error", err)
		return filepath.Join(".config", "randwall")
	}
	return filepath.Join(home, ".config", "randwall")
}

func Load() *Config {
	cfg := defaultConfig()
	cfg.path = filepath.Join(configDir(), "config.json")

	if data, err := os.ReadFile(cfg.path); err == nil {
		if err := json.Unmarshal(data, cfg); err != nil {
			slog.Warn("error reading config, using defaults", "error", err)
		}
	} else {
		slog.Info("no config found, creating default", "path", cfg.path)
	}

	cfg.save()
	go cfg.watch()
	return cfg
}

func (c *Config) save() {
	if err := os.MkdirAll(filepath.Dir(c.path), 0755); err != nil {
		slog.Error("error creating config directory", "error", err)
		return
	}
	data, err := json.MarshalIndent(c, "", "  ")
	if err != nil {
		slog.Error("error marshaling config", "error", err)
		return
	}
	if err := os.WriteFile(c.path, data, 0644); err != nil {
		slog.Error("error writing config", "error", err)
	}
}

func (c *Config) watch() {
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		slog.Error("error creating config watcher", "error", err)
		return
	}
	defer watcher.Close()

	if err := watcher.Add(c.path); err != nil {
		slog.Error("error watching config file", "error", err)
		return
	}

	for range watcher.Events {
		data, err := os.ReadFile(c.path)
		if err != nil {
			continue
		}
		if err := json.Unmarshal(data, c); err != nil {
			slog.Error("error reloading config", "error", err)
			continue
		}
		slog.Info("config reloaded")
	}
}
