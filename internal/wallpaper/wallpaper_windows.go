//go:build windows

package wallpaper

import (
	"syscall"
	"unsafe"
)

func setWallpaper(path string) error {
	user32 := syscall.NewLazyDLL("user32.dll")
	systemParametersInfo := user32.NewProc("SystemParametersInfoW")

	pathPtr, err := syscall.UTF16PtrFromString(path)
	if err != nil {
		return err
	}

	_, _, err = systemParametersInfo.Call(
		0x0014, // SPI_SETDESKWALLPAPER
		0,
		uintptr(unsafe.Pointer(pathPtr)),
		0x0002, // SPIF_SENDCHANGE
	)

	if err != syscall.Errno(0) {
		return err
	}
	return nil
}
