import os

from setuptools import find_packages, setup  # type: ignore

version = os.environ.get("RELEASE_VERSION", "0.0.1")


def read_requirements():
    with open("requirements.txt") as req:
        return req.read().splitlines()


setup(
    name="rated-parser",
    version='1.0.0',
    python_requires=">=3.6",
    install_requires=read_requirements(),
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["tests", "tests.*"]),
    long_description="Rated Parser is a flexible log parsing tool designed "
    "to extract meaningful insights from complex log structures with ease.",
)
