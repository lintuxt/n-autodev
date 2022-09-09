from nautodev.settings import Settings
from nautodev.dispatcher import Dispatcher
from nautodev.vault import Vault
from nautodev.project import Project
from nautodev.run import Run


def main():
    settings = Settings().settings
    vault = Vault(settings)
    project = Project(settings)
    run = Run(settings)
    Dispatcher().run(
        delegate={
            "vault": {
                "init": vault.initialize_vault,
                "status": vault.vault_status,
                "list-secrets": vault.vault_list_secrets,
                "create-secret": vault.vault_create_secret,
                "show-secret": vault.vault_show_secret,
                "delete-secret": vault.vault_delete_secret,
            },
            "project": {
                "init": project.initialize_project,
            },
            "run": {
                "command": run.run_command,
            },
        }
    )


if __name__ == "__main__":
    main()
