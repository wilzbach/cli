import os
import json

import appdirs

CACHE_DIR = appdirs.user_cache_dir(
    appname='storyscript-cli', appauthor='asyncy'
)
STORAGE_DIR = appdirs.user_state_dir(
    appname='storyscript-cli', appauthor='asyncy'
)


class Storage:
    def __init__(self, path):
        self.path = path
        self._data = {}

        self._touch()
        self._load()

    def _touch(self):
        # Make the directory, if it doesn't exist.
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        # Touch the file.
        with open(self.path, 'a') as f:
            f.write('')

    def _load(self):
        with open(self.path, 'r') as f:
            try:
                self._data.update(json.load(f))
            except ValueError:
                pass

    def _save(self):
        with open(self.path, 'w') as f:
            json.dump(self._data, f)

    def fetch(self, key, default=None):
        return self._data.get(key, default)

    def store(self, key, value):
        self._data[key] = value
        self._save()

    def delete(self, key):
        del self._data[key]
        self._save()

    def as_dict(self):
        return self._data

    def change_path(self, p):
        self.path = p
        self._load()

    def __contains__(self, *args, **kwargs):
        return self._data.__contains__(*args, **kwargs)


cache_loc = os.path.join(CACHE_DIR, 'cache.json')
cache = Storage(path=cache_loc)

config_loc = os.path.join(STORAGE_DIR, 'config.json')
config = Storage(path=config_loc)
