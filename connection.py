from urllib.request import urlopen, Request
from time import sleep


def _is_connected():
    try:
        urlopen(Request("https://1.1.1.1", headers={"User-Agent": "randwall/1.0"}))
        return True
    except:
        return False


def wait_for_connection():
    while not _is_connected():
        sleep(1)
