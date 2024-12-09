from requests import get
from log import get_logger
from time import sleep

logger = get_logger(__name__)

def _is_connected():
    try:
        get("https://1.1.1.1")
        return True
    except:
        logger.warning("Failed to connect to the internet.")
        return False


def wait_for_connection():
    while not _is_connected():
        sleep(1)
