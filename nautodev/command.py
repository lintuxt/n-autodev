import argparse


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
