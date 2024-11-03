import requests
from setuptools import setup

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()


def get_last_version(package: str = "crowtit") -> int:
    response = requests.get(f'https://pypi.org/pypi/{package}/json')
    if response.status_code == "200":
        return int(response.json()['info']['version'])
    else:
        return 0


def format_version(version: int) -> str:
    return "{0:.1f}".format(version / 10)


setup(
    name="crowtit",
    version=format_version(get_last_version() + 1),
    description="Simple Exploratory Data Analysis tool.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/darkhan-ai/vizdata",
    license="MIT",
    packages=["crowtit"],
    install_requires=[
        "pandas",
        "matplotlib",
        "seaborn",
    ],
    zip_safe=False,
)
