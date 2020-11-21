from appdirs import user_config_dir
import json
from os import path, makedirs
from log import get_logger

logger = get_logger(__name__)

config_dir = user_config_dir(appname="randwall")
if not path.exists(config_dir):
    makedirs(config_dir)

config_file_path = f'{config_dir}/config.json'
if not path.exists(config_file_path):
    logger.info(f"Creating default config at {config_file_path}")

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
        }
    }

    with open(config_file_path, 'wt') as f:
        json.dump(default_config, f, sort_keys=True, indent=2)

with open(config_file_path, 'rt') as f:
    logger.info(f"Reading config from {config_file_path}")
    config = json.load(f)
