import os
from setuptools import setup

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="smartoutlet",
    version="0.4.0",
    description="Collection of utilities for interfacing with various PDUs and smart outlets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DragonMinded",
    author_email="dragonminded@dragonminded.com",
    license="Public Domain",
    url="https://github.com/DragonMinded/smartoutlet",
    package_data={"smartoutlet": ["py.typed"]},
    packages=[
        "smartoutlet",
    ],
    install_requires=[
        "requests",
        "pyasyncore",
        "pysnmplib",
        "flask",
    ],
    python_requires=">=3.6",
)
