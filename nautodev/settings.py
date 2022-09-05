import os

from pathlib import Path

from configparser import ConfigParser


class Settings(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            base_dir = Path(__file__).resolve().parent
            config_file = os.path.join(base_dir, "settings.ini")
            config = ConfigParser()
            config.read(config_file)
            cls._instance.settings = config
        return cls._instance
