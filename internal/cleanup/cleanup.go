package cleanup

import (
	"log/slog"
	"os"
	"path/filepath"
	"sort"

	"github.com/arch-anes/randwall/internal/config"
)

type Queue struct {
	items []string
	cfg   *config.Config
}

func New(cfg *config.Config) *Queue {
	q := &Queue{cfg: cfg}
	q.loadExisting()
	return q
}

func (q *Queue) loadExisting() {
	dir := filepath.Join(os.TempDir(), "randwall")
	entries, err := os.ReadDir(dir)
	if err != nil {
		return
	}

	var files []struct {
		path string
		time int64
	}
	for _, e := range entries {
		if e.IsDir() {
			continue
		}
		info, err := e.Info()
		if err != nil {
			continue
		}
		files = append(files, struct {
			path string
			time int64
		}{
			path: filepath.Join(dir, e.Name()),
			time: info.ModTime().Unix(),
		})
	}

	sort.Slice(files, func(i, j int) bool {
		return files[i].time < files[j].time
	})

	for _, f := range files {
		q.items = append(q.items, f.path)
	}

	q.cleanup()
}

func (q *Queue) Enqueue(path string) {
	q.items = append(q.items, path)
	q.cleanup()
}

func (q *Queue) cleanup() {
	if q.cfg.Keep == 0 {
		return
	}

	for len(q.items) > q.cfg.Keep {
		old := q.items[0]
		q.items = q.items[1:]

		if old != "" {
			slog.Info("removing wallpaper", "path", old)
			os.Remove(old)
		}
	}
}
