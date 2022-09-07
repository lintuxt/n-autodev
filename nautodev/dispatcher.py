import argparse


class ShowActionParser(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(ShowActionParser, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, "show-secret")
        setattr(namespace, "operands", values)


class DeleteActionParser(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(DeleteActionParser, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, "delete-secret")
        setattr(namespace, "operands", values)


class Command:
    def __init__(self):
        self._parser = argparse.ArgumentParser(
            allow_abbrev=False,
            prog="nautodev",
            description="nautodev is a tool to automate development tasks.",
            epilog="Go to https://github.com/lintuxt/n-autodev for more information.",
        )
        self._parser.version = "0.0.1"
        self._parser.add_argument("--version", action="version")
        self._subparsers = None
        self._subcommands = {}
        self._subcommands_exclusive_group = {}

    def add_subcommand(self, subcommand, **kwargs):
        if self._subparsers is None:
            self._subparsers = self._parser.add_subparsers(help="sub-commands", dest="subcommand")
        if self._subcommands.get(subcommand) is None:
            self._subcommands[subcommand] = self._subparsers.add_parser(subcommand, **kwargs)

    def add_argument(self, subcommand, *args, **kwargs):
        if self._subcommands.get(subcommand) is not None:
            self._subcommands[subcommand].add_argument(*args, **kwargs)
        else:
            raise SystemExit("There was an internal error. Please contact the developer. E1003")

    def add_exclusive_argument(self, subcommand, *args, **kwargs):
        if self._subcommands.get(subcommand) is not None:
            sc_parser = self._subcommands[subcommand]
            if self._subcommands_exclusive_group.get(subcommand) is None:
                self._subcommands_exclusive_group[
                    subcommand
                ] = sc_parser.add_mutually_exclusive_group()
            self._subcommands_exclusive_group[subcommand].add_argument(*args, **kwargs)
        else:
            raise SystemExit("There was an internal error. Please contact the developer. E1002")

    def parse_args(self):
        return self._parser.parse_args()

    def print_help(self, subcommand=None):
        if subcommand is None:
            self._parser.print_help()
        elif self._subcommands.get(subcommand) is not None:
            self._subcommands[subcommand].print_help()


class Dispatcher:
    def __init__(self):
        self.command = Command()
        self.command.add_subcommand(
            "vault", allow_abbrev=False, help="It securely stores secrets locally."
        )
        self.command.add_exclusive_argument(
            "vault",
            "--init",
            action="store_const",
            const="init",
            dest="argument",
            help="initializes the vault",
        )
        self.command.add_exclusive_argument(
            "vault",
            "--status",
            action="store_const",
            const="status",
            dest="argument",
            help="shows if the vault is initialized",
        )
        self.command.add_exclusive_argument(
            "vault",
            "--list-secrets",
            action="store_const",
            const="list-secrets",
            dest="argument",
            help="list all stored secrets",
        )
        self.command.add_exclusive_argument(
            "vault",
            "--create-secret",
            action="store_const",
            const="create-secret",
            dest="argument",
            help="create a new secret",
        )
        self.command.add_exclusive_argument(
            "vault",
            "--show-secret",
            action=ShowActionParser,
            nargs=1,
            dest="argument",
            metavar="KEY",
            help="show a secret",
        )
        self.command.add_exclusive_argument(
            "vault",
            "--delete-secret",
            action=DeleteActionParser,
            nargs=1,
            dest="argument",
            metavar="KEY",
            help="delete a secret",
        )

    def run(self, delegate=None):
        if delegate is None:
            raise SystemExit("There was an internal error. Please contact the developer. E1000")

        args = self.command.parse_args()
        try:
            if "operands" in args and args.operands is not None:
                delegate[args.subcommand][args.argument](args.operands[0])
            else:
                delegate[args.subcommand][args.argument]()
        except KeyError:
            self.command.print_help(args.subcommand)
