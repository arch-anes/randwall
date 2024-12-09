from watchfiles import watch
from threading import Thread
from platformdirs import user_config_dir
import json
from os import path, makedirs
from log import get_logger

logger = get_logger(__name__)


class Config:
    config_dir = user_config_dir(appname="randwall")
    config_file_path = f'{config_dir}/config.json'

    default_config = {
        'api_key': '',
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
        "tags": "-microsoft -logo +trees",
        'interval': 30,
        'keep': 10,

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
            logger.info(f"No config file found at {self.config_file_path}. Loading default config...")
            return self.default_config

        with open(self.config_file_path, 'rt') as f:
            logger.info(f"Reading config from {self.config_file_path}")
            try:
                loaded_config = json.load(f)
                return {**self.default_config, **loaded_config}
            except:
                logger.error(f"An error occured when reading config from {self.config_file_path}. Loading default config...")
                return self.default_config

    def _watch_config_changes(self):
        def watch_config():
            for changes in watch(self.config_file_path):
                self.raw_config = self._load_config()

        thread = Thread(target=watch_config)
        thread.daemon = True
        thread.start()


config = Config()
