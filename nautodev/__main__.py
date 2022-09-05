import os.path
from pathlib import Path

from configparser import ConfigParser

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = os.path.join(BASE_DIR, "config.ini")


def main():
    config = ConfigParser()
    config.read(CONFIG_FILE)
    print(config["default"]["welcome_message"])


if __name__ == "__main__":
    main()
