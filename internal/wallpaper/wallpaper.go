package wallpaper

import (
	"encoding/json"
	"fmt"
	"io"
	"log/slog"
	"math/rand/v2"
	"net/http"
	"net/url"
	"os"
	"path/filepath"

	"github.com/arch-anes/randwall/internal/config"
)

type wallpaper struct {
	ID   string
	URL  string
	Path string
}

func SetRandom(cfg *config.Config) string {
	wp, err := fetchRandom(cfg)
	if err != nil {
		return ""
	}

	path, err := download(wp)
	if err != nil {
		return ""
	}

	set(wp, path)
	return path
}

func fetchRandom(cfg *config.Config) (*wallpaper, error) {
	page := rand.IntN(cfg.MaxPage) + 1
	apiURL := fmt.Sprintf("https://wallhaven.cc/api/v1/search?apikey=%s&categories=%s&purity=%s&q=%s&sorting=%s&topRange=1y&page=%d&ratios=16x9,16x10&atleast=%s",
		cfg.APIKey,
		dictToBinary(cfg.Categories, []string{"general", "anime", "people"}),
		dictToBinary(cfg.Purity, []string{"sfw", "sketchy", "nsfw"}),
		url.QueryEscape(cfg.Tags),
		cfg.Sorting,
		page,
		cfg.MinResolution)

	slog.Info("fetching random wallpaper from https://wallhaven.cc")

	req, err := http.NewRequest(http.MethodGet, apiURL, nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("User-Agent", "randwall/1.0")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		slog.Error("couldn't fetch wallpaper", "error", err)
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		slog.Error("API returned error", "status", resp.StatusCode, "body", string(body))
		return nil, fmt.Errorf("API error: status %d", resp.StatusCode)
	}

	var result struct {
		Data []struct {
			ID   string `json:"id"`
			URL  string `json:"url"`
			Path string `json:"path"`
		} `json:"data"`
		Meta struct {
			CurrentPage int `json:"current_page"`
			LastPage    int `json:"last_page"`
		} `json:"meta"`
	}

	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		slog.Error("couldn't parse wallpaper response", "error", err)
		return nil, err
	}

	if len(result.Data) == 0 {
		return nil, fmt.Errorf("no wallpapers found")
	}

	slog.Info("fetched wallpaper", "page", result.Meta.CurrentPage)

	if result.Meta.LastPage < cfg.MaxPage {
		slog.Warn("last page is lower than configured max_page", "last_page", result.Meta.LastPage, "max_page", cfg.MaxPage)
	}

	idx := rand.IntN(len(result.Data))
	return &wallpaper{
		ID:   result.Data[idx].ID,
		URL:  result.Data[idx].URL,
		Path: result.Data[idx].Path,
	}, nil
}

func download(wp *wallpaper) (string, error) {
	dir := filepath.Join(os.TempDir(), "randwall")
	if err := os.MkdirAll(dir, 0755); err != nil {
		return "", err
	}
	path := filepath.Join(dir, wp.ID+".jpg")

	slog.Info("downloading wallpaper", "url", wp.URL, "path", path)

	resp, err := http.Get(wp.Path)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	f, err := os.Create(path)
	if err != nil {
		return "", err
	}
	defer f.Close()

	if _, err := io.Copy(f, resp.Body); err != nil {
		return "", err
	}

	return path, nil
}

func set(wp *wallpaper, path string) {
	slog.Info("setting wallpaper", "id", wp.ID)
	if err := setWallpaper(path); err != nil {
		slog.Error("error setting wallpaper", "error", err)
	}
}

func dictToBinary(m map[string]bool, order []string) string {
	var b []byte
	for _, key := range order {
		if m[key] {
			b = append(b, '1')
		} else {
			b = append(b, '0')
		}
	}
	return string(b)
}
