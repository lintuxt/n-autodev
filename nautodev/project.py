import os
import yaml


class Project:
    def __init__(self, settings):
        self._settings = settings
        self._initial_nautodev_file_name = self._settings["main"]["initial_nautodev_file"]
        self._initial_nautodev_file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), self._initial_nautodev_file_name
        )

    def _load_project_file(self):
        if not os.path.exists(self._initial_nautodev_file_path):
            raise SystemExit("There was an internal error. Please contact the developer. E1025")
        with open(self._initial_nautodev_file_path, "rb") as file:
            self._nautodev_file = file.read()

    def initialize_project(self):
        self._load_project_file()
        yaml_data = yaml.safe_load(self._nautodev_file)
        print(yaml.dump(yaml_data, default_flow_style=False, sort_keys=False))
