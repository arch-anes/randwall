//go:build !windows && !darwin

package wallpaper

import "github.com/xyproto/wallutils"

func setWallpaper(path string) error {
	return wallutils.SetWallpaper(path)
}
