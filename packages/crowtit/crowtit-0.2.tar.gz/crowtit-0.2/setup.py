"""NOTE:
    1. For simplicity version has *.d format, e.g.: 0.1, 0.2, 1.7.
    2. Will automatically publish new version by github action jobs.
"""

import requests
from setuptools import setup

PACKAGE_NAME = "crowtit"
with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()


def get_last_version() -> int:
    """
    :return: version multiplied to 10.
    """
    response = requests.get(f'https://pypi.org/pypi/{PACKAGE_NAME}/json')
    if response.status_code == 200:
        current_version = float(response.json()['info']['version'])
        return int(current_version * 10)
    else:
        return 0


def format_version(version: int) -> str:
    return "{0:.1f}".format(version / 10)


setup(
    name=PACKAGE_NAME,
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
