import platform
import os
from log import get_logger
from requests import get
from config import config
import subprocess
import tempfile

logger = get_logger(__name__)

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
        command_dark = subprocess.call(
            ["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", "file://" + wallpaper_path], **silent)
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


def _dict_to_binary_string(d):
    return ''.join((str(int(val)) for val in d.values()))


def _get_random_wallpaper():
    api_url = "https://wallhaven.cc/api/v1/search"
    params = {
        "categories": _dict_to_binary_string(config['categories']),
        "purity": _dict_to_binary_string(config['purity']),
        "q": config['tags'],
        "sorting": "random",
        "topRange": "1y",
        "page": "1",
        "ratios": "16x9,16x10",
    }
    headers = {
        "User-Agent": "randwall/1.0"
    }

    try:
        response = get(api_url, params=params, headers=headers)
        data = response.json()
        image_data = data["data"][0]
        return {"id": image_data["id"], "url": image_data['path']}
    except:
        logger.error("Couldn't fetch wallpaper.")


def _download_wallpaper(wallpaper):
    image_dir = tempfile.gettempdir()
    image_path = f"{image_dir}/{wallpaper['id']}.jpg"

    logger.info(f"Downloading {wallpaper['url']} at {image_path}")

    try:
        image = get(wallpaper['url']).content
    except:
        return

    with open(image_path, 'wb') as f:
        f.write(image)

    return image_path


def set_random_wallpaper():
    wallpaper = _get_random_wallpaper()
    if wallpaper is None:
        return

    wallpaper_path = _download_wallpaper(wallpaper)
    if wallpaper_path is None:
        return

    _set_wallpaper(wallpaper, wallpaper_path)
    return wallpaper_path
