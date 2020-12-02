from watchgod import watch
from threading import Thread
import sys
from appdirs import user_config_dir
import json
from os import path, makedirs
from log import get_logger

logger = get_logger(__name__)


class Config:
    config_dir = user_config_dir(appname="randwall")
    config_file_path = f'{config_dir}/config.json'

    default_config = {
        'api_key': '',
        'keep': 10,
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

    def __init__(self):
        self.raw_config = self._load_config()
        self._write_config()
        self._watch_config_changes()

    def __getitem__(self, arg):
        return self.raw_config[arg]

    def _write_config(self):
        if not path.exists(self.config_dir):
            makedirs(self.config_dir)

        logger.info(f"Writing config to {self.config_file_path}")
        with open(self.config_file_path, 'wt') as f:
            json.dump(self.raw_config, f, sort_keys=True, indent=2)

    def _load_config(self):
        if not path.exists(self.config_file_path):
            return self.default_config

        with open(self.config_file_path, 'rt') as f:
            logger.info(f"Reading config from {self.config_file_path}")
            try:
                loaded_config = json.load(f)
                return {**self.default_config, **loaded_config}
            except:
                logger.error(f"An error occured when reading config from {self.config_file_path}")

    def _watch_config_changes(self):
        def watch_config():
            for changes in watch(self.config_file_path):
                self.raw_config = self._load_config()

        thread = Thread(target=watch_config)
        thread.daemon = True
        thread.start()


config = Config()
