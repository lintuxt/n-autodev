import argparse


class VaultShowSecretActionParser(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(VaultShowSecretActionParser, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, "show-secret")
        setattr(namespace, "operands", values)


class VaultDeleteSecretActionParser(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(VaultDeleteSecretActionParser, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, "delete-secret")
        setattr(namespace, "operands", values)


class RunCommandActionParser(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(RunCommandActionParser, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, "command")
        setattr(namespace, "operands", values)
