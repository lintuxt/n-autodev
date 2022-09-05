# from .settings import Settings
from .dispatcher import CommandLineDispatcher


def main():
    # settings = Settings().settings
    command_line = CommandLineDispatcher()
    command_line.parser.parse_args()


if __name__ == "__main__":
    main()
