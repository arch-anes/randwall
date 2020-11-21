from watchgod import watch
from threading import Thread
import sys
from appdirs import user_config_dir
import json
from os import path, makedirs
from log import get_logger

logger = get_logger(__name__)

default_config = {
    'api_key': '',
    'max_page': 500,
    'interval': 30,
    'categories': {
        'general': True,
        'anime': True,
        'people': True,
    },
    'purity': {
        'sfw': True,
        'sketchy': False,
        'nsfw': False,
    },
    'include': [],
    'exclude': ['microsoft', 'logo'],
}

config_dir = user_config_dir(appname="randwall")
if not path.exists(config_dir):
    makedirs(config_dir)

config_file_path = f'{config_dir}/config.json'
if not path.exists(config_file_path):
    logger.info(f"Creating default config at {config_file_path}")

    with open(config_file_path, 'wt') as f:
        json.dump(default_config, f, sort_keys=True, indent=2)


class Config:
    def __init__(self):
        self.raw_config = self._load_config()

    def _load_config(self):
        with open(config_file_path, 'rt') as f:
            logger.info(f"Reading config from {config_file_path}")
            try:
                loaded_config = json.load(f)
                return {**default_config, **loaded_config}
            except:
                logger.error(f"An error occured when reading config from {config_file_path}")

    def watch_config_changes(self):
        for changes in watch(config_file_path):
            self.raw_config = self._load_config()


config = Config()


thread = Thread(target=config.watch_config_changes)
thread.daemon = True
thread.start()
