from pathlib import Path
from setuptools import setup

# The directory containing this file
HERE = Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="n-autodev",
    version="0.0.1",
    description="Automation tools for development.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/lintuxt/n-autodev",
    author="Alexis Charytonow",
    author_email="alexis@nodeux.com",
    license="MIT",
    packages=["nautodev"],
    include_package_data=True,
    install_requires=["cryptography"],
    entry_points={
        "console_scripts": [
            "nautodev=nautodev.__main__:main",
        ]
    },
)
