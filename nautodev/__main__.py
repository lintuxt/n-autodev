from nautodev.settings import Settings
from nautodev.dispatcher import Dispatcher
from nautodev.vault import Vault


def main():
    settings = Settings().settings
    vault = Vault(settings)
    Dispatcher().run(
        delegate={
            "vault": {
                "init": vault.initialize_vault,
                "status": vault.vault_status,
                "list-secrets": vault.vault_list_secrets,
                "create-secret": vault.vault_create_secret,
                "show-secret": vault.vault_show_secret,
                "delete-secret": vault.vault_delete_secret,
            }
        }
    )


if __name__ == "__main__":
    main()
