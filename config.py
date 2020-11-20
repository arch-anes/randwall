from appdirs import user_config_dir
import json
from os import path, makedirs

config_dir = user_config_dir(appname="random_wallpaper")
if not path.exists(config_dir):
    makedirs(config_dir)

config_file_path = f'{config_dir}/config.json'
if not path.exists(config_file_path):
    default_config = {
        'max_page': 500,
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
        json.dump(default_config, f)

with open(config_file_path, 'rt') as f:
    config = json.load(f)
