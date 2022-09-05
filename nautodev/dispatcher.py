import argparse


class CommandLineDispatcher:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="n-autodev is a tool to automate development tasks."
        )
        # self.parser.add_argument("command", help="Subcommand to run")
