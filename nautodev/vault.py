import os
import yaml

from pathlib import Path
from cryptography.fernet import Fernet


class Vault:
    def __init__(self, settings):
        self._vault = None
        self._settings = settings
        self._system_folder_name = self._settings["system"]["system_folder"]
        self._system_folder_path = os.path.join(os.path.expanduser("~"), self._system_folder_name)
        self._encryption_key_file_name = self._settings["vault"]["encryption_key_file"]
        self._encryption_key_file_path = os.path.join(
            self._system_folder_path, self._encryption_key_file_name
        )
        self._vault_file_name = self._settings["vault"]["vault_file"]
        self._vault_file_path = os.path.join(self._system_folder_path, self._vault_file_name)
        self._initial_vault_file_name = self._settings["vault"]["initial_vault_file"]
        self._initial_vault_file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), self._initial_vault_file_name
        )

    def _encrypt(self, data):
        if not os.path.exists(self._encryption_key_file_path):
            raise SystemExit(
                "Encryption key file not found at {}".format(self._encryption_key_file_path)
            )
        with open(self._encryption_key_file_path, "rb") as file:
            key = file.read()
        f = Fernet(key)
        return f.encrypt(data.encode())

    def _decrypt(self, data):
        if not os.path.exists(self._encryption_key_file_path):
            raise SystemExit(
                "Encryption key file not found at {}".format(self._encryption_key_file_path)
            )
        with open(self._encryption_key_file_path, "rb") as file:
            key = file.read()
        f = Fernet(key)
        return f.decrypt(data).decode()

    def _initialize_system_folder(self):
        print("[+] Initializing vault at {}".format(self._system_folder_path))
        Path(self._system_folder_path).mkdir(parents=True, exist_ok=True)

    def _initialize_encryption_key(self):
        if not os.path.exists(self._encryption_key_file_path):
            key = Fernet.generate_key()
            with open(self._encryption_key_file_path, "wb") as file:
                file.write(key)
            print("[+] Encryption key initialized at {}".format(self._encryption_key_file_path))
        else:
            print("[OK] Encryption key already exists at {}".format(self._encryption_key_file_path))

    def _load_initial_vault(self):
        with open(self._initial_vault_file_path, "r") as file:
            self._vault = file.read()

    def _save_vault(self):
        if self._vault is None:
            raise SystemExit("There was an internal error. Please contact the developer. E1001")
        with open(self._vault_file_path, "wb") as file:
            file.write(self._encrypt(self._vault))

    def _initialize_vault_file(self):
        if not os.path.exists(self._vault_file_path):
            self._load_initial_vault()
            self._save_vault()
            print("[+] Vault file initialized at {}".format(self._vault_file_path))
        else:
            print("[OK] Vault file already exists at {}".format(self._vault_file_path))

    def _load_vault(self):
        if not os.path.exists(self._vault_file_path):
            raise SystemExit("Vault file not found at {}".format(self._vault_file_path))
        with open(self._vault_file_path, "rb") as file:
            self._vault = self._decrypt(file.read())

    def initialize_vault(self):
        self._initialize_system_folder()
        self._initialize_encryption_key()
        self._initialize_vault_file()

    def vault_status(self):
        if not os.path.exists(self._encryption_key_file_path):
            print("[!] Encryption key file not found at {}".format(self._encryption_key_file_path))
        else:
            print("[OK] Encryption key file found at {}".format(self._encryption_key_file_path))

        if not os.path.exists(self._vault_file_path):
            print("[!] Vault is not initialized. Run 'nautodev vault --init' to initialize it.")
        else:
            print("[OK] Vault file found at {}".format(self._vault_file_path))

    def vault_list_secrets(self):
        self._load_vault()
        print(self._vault)

    def vault_create_secret(self):
        self._load_vault()
        yaml_vault_dict = yaml.safe_load(self._vault)
        print("[+] Please, enter the following information:")
        key = input("key: ")
        secret = input("secret: ")
        print("Reading back key/secret for verification:")
        print("key: {}".format(key))
        print("secret: {}".format(secret))
        is_correct = input("Is this correct? [y/N]: ")
        if is_correct.lower() == "y":
            secret_object = {"key": key, "secret": secret}
            yaml_vault_dict["vault"].append(secret_object)
            self._vault = yaml.dump(yaml_vault_dict, default_flow_style=False, sort_keys=False)
            self._save_vault()
            print("[+] Secret saved.")
        else:
            print("[!] Secret not saved.")

    def vault_get_secret(self, key):
        self._load_vault()
        yaml_vault_dict = yaml.safe_load(self._vault)
        for secret in yaml_vault_dict["vault"]:
            if secret["key"] == key:
                return secret["secret"]
        return None

    def vault_show_secret(self, args):
        key = args[0]
        secret = self.vault_get_secret(key)
        if secret:
            print(secret)
        else:
            print("[!] Secret not found.")

    def vault_delete_secret(self, args):
        key = args[0]
        self._load_vault()
        yaml_vault_dict = yaml.safe_load(self._vault)
        for secret in yaml_vault_dict["vault"]:
            if secret["key"] == key:
                yaml_vault_dict["vault"].remove(secret)
                self._vault = yaml.dump(yaml_vault_dict, default_flow_style=False, sort_keys=False)
                self._save_vault()
                print("[+] Secret deleted.")
                return True
        print("[!] Secret not found.")
