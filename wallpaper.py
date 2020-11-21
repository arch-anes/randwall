from wallhaven import Wallhaven, Parameters
from random import randint, choice
import platform
import os
from log import get_logger
from requests import get
from config import config
import subprocess

logger = get_logger(__name__)

wallhaven = Wallhaven()
wallhaven.REQUEST_TIMEOUT = 0


# Taken from https://github.com/AlfredoSequeida/venus/blob/master/venus/os_tools/

def _set_wallpaper_macos(wallpaper_path):
    SCRIPT = """/usr/bin/osascript<<END
    tell application "Finder"
    set desktop picture to POSIX file "%s"
    end tell"""

    subprocess.Popen(SCRIPT % wallpaper_path, shell=True)


def _set_wallpaper_linux(wallpaper_path):
    silent = dict(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        command = subprocess.call(
            ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "file://" + wallpaper_path], **silent)
    except:
        pass

    try:
        feh = subprocess.call(["feh", "--bg-fill", wallpaper_path], **silent)
    except:
        pass

    try:
        import dbus

        plugin = 'org.kde.image'

        jscript = """
		var allDesktops = desktops();
		print (allDesktops);
		for (i=0;i<allDesktops.length;i++) {
			d = allDesktops[i];
			d.wallpaperPlugin = "%s";
			d.currentConfigGroup = Array("Wallpaper", "%s", "General");
			d.writeConfig("Image", "file://%s")
		}
		"""
        bus = dbus.SessionBus()
        plasma = dbus.Interface(bus.get_object(
            'org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
        plasma.evaluateScript(jscript % (plugin, plugin, wallpaper_path))

    except:
        pass

    try:
        swaymsg = subprocess.call(["swaymsg", "output * bg \"{f}\" fill".format(f=wallpaper_path)], **silent)
    except:
        pass


def _set_wallpaper_windows(wallpaper_path):
    import ctypes

    SPI = 20
    SPIF = 2

    ctypes.windll.user32.SystemParametersInfoW(SPI, 0, wallpaper_path, SPIF)


def _set_wallpaper(wallpaper, wallpaper_path):
    logger.info(f"Setting {wallpaper['id']} as current wallpaper")

    if platform.system() == 'Linux':
        _set_wallpaper_linux(wallpaper_path)
    if platform.system() == 'Darwin':
        _set_wallpaper_macos(wallpaper_path)
    if platform.system() == 'Windows':
        _set_wallpaper_windows(wallpaper_path)


def _get_random_wallpaper():
    params = Parameters()
    params.set_categories(**config['categories'])
    params.set_sorting("toplist")
    params.set_range("1y")
    params.set_purity(**config['purity'])
    params.set_page(randint(1, config['max_page']))

    data = wallhaven.search(params)

    return choice(data)


def _download_wallpaper(wallpaper, image_dir):
    image_path = f"{image_dir}/{wallpaper['id']}.jpg"

    logger.info(f"Downloading {wallpaper['url']} at {image_path}")

    with open(image_path, 'wb') as f:
        image = get(wallpaper['path']).content
        f.write(image)

    return image_path


def set_random_wallpaper(image_dir):
    wallpaper = _get_random_wallpaper()
    wallpaper_path = _download_wallpaper(wallpaper, image_dir)
    _set_wallpaper(wallpaper, wallpaper_path)
