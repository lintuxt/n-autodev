import os
import yaml

from pathlib import Path

from nautodev.vault import Vault


class Run:
    def __init__(self, settings):
        self._settings = settings
        self._nautodev_file_name = self._settings["main"]["nautodev_file"]
        self._nautodev_file_path = os.path.join(Path.cwd(), self._nautodev_file_name)
        self._vault = None

    def _load_nautodev_file(self):
        try:
            with open(self._nautodev_file_path, "rb") as file:
                self._nautodev_file = file.read()
        except FileNotFoundError:
            raise SystemExit("[!] Nautodev file not found at {}".format(self._nautodev_file_path))

    def run_command(self, command):
        self._load_nautodev_file()
        yaml_data = yaml.safe_load(self._nautodev_file)

        if "vault" in yaml_data:
            if "keys" in yaml_data["vault"]:
                self._vault = Vault(self._settings)
                for key in yaml_data["vault"]["keys"]:
                    secret = self._vault.vault_get_secret(key)
                    if secret:
                        formatted_key = key.replace("-", "_").upper()
                        os.environ[formatted_key] = secret

        for found_command in yaml_data["commands"]:
            if command[0] in found_command:
                os.system(found_command[command[0]])
                exit(0)

        raise SystemExit("[!] Command not found.")
