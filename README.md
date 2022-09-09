# n-autodev

### v-0.0.1 - alpha

This tool allows you to run commands declared on a YAML file with secrets that are securely stored on your local machine.

Disclaimer: This is a work in progress. It is not ready for production use.

LICENSE: MIT

Note: make sure to use a virtual-env, pyenv or conda to avoid polluting your system python.

usage:
1) Clone this repo.
2) `cd n-autodev`
3) `pip install .`
4) `nautodev --help`
5) `nautodev project --init > nautodev.yaml`
6) `nautodev run --command echo`
7) `nautodev run --command decrypt-me-echo`

Soon to be published on PyPI.

by: @lintuxt
