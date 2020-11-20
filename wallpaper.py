from wallhaven import Wallhaven, Parameters
from random import randint, choice
import platform
import os
from log import get_logger
from requests import get


logger = get_logger(__name__)

wallhaven = Wallhaven()
wallhaven.REQUEST_TIMEOUT = 0


def _set_wallpaper(wallpaper, wallpaper_path):
    logger.info(f"Setting {wallpaper['id']} as current wallpaper")

    if platform.system() == 'Linux':
        os.system(f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri {wallpaper_path}")
    else:
        import wallpaper
        wallpaper.set_wallpaper(wallpaper_path)


def _get_random_wallpaper(wallhaven_max_page):
    params = Parameters()
    params.set_categories(general=True, anime=True, people=True)
    params.set_sorting("toplist")
    params.set_range("1y")
    params.set_purity(sfw=True, sketchy=True, nsfw=True)
    params.set_page(randint(1, wallhaven_max_page))

    data = wallhaven.search(params)

    return choice(data)


def _download_wallpaper(wallpaper, image_dir):
    logger.info(f"Downloading {wallpaper['url']}")

    image_path = f"{image_dir}/{wallpaper['id']}.jpg"

    with open(image_path, 'wb') as f:
        image = get(wallpaper['path']).content
        f.write(image)

    return image_path


def set_random_wallpaper(wallhaven_max_page, image_dir):
    wallpaper = _get_random_wallpaper(wallhaven_max_page)
    wallpaper_path = _download_wallpaper(wallpaper, image_dir)
    _set_wallpaper(wallpaper, wallpaper_path)
