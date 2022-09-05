import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="nautodev",
    version="0.0.1",
    description="This allows you to automate your dev environment by using capsules.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/lintuxt/py-capsule",
    author="Alexis Charytonow",
    author_email="alexis@nodeux.com",
    license="MIT",
    classifiers=["License :: MIT License"],
    packages=["nautodev"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "capsulecorp=nautodev.__main__:main",
        ]
    },
)
