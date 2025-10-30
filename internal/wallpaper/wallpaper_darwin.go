//go:build darwin

package wallpaper

import "os/exec"

func setWallpaper(path string) error {
	script := `tell application "Finder" to set desktop picture to POSIX file "` + path + `"`
	return exec.Command("/usr/bin/osascript", "-e", script).Run()
}
