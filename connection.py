from requests import get
from time import sleep


def _is_connected():
    try:
        get("https://1.1.1.1")
        return True
    except:
        return False


def wait_for_connection():
    while not _is_connected():
        sleep(1)
