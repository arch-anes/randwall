from queue import Queue
from config import config
import os
from log import get_logger

logger = get_logger(__name__)

queue = Queue()


def enqueue_wallpaper_for_cleanup(wallpaper_path):
    max_queue_size = config["keep"]

    queue.put(wallpaper_path)

    if max_queue_size == 0:
        return

    while queue.qsize() > max_queue_size:
        wallpaper = queue.get()
        if os.path.exists(wallpaper):
            logger.info(f"Removing {wallpaper}")
            os.remove(wallpaper)
