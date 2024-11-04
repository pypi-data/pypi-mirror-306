from pathlib import Path
from setuptools import setup, find_packages
import sys

sys.path.insert(0, ".")

import icutk

VERSION = icutk.__version__
DESCRIPTION = "Integrated Circuit Utilities (kit)"
PROJECT = "icutk"
AUTHOR = "YEUNGCHIE"

setup(
    name=PROJECT,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=Path("README.md").read_text("utf-8"),
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR.lower()}/{PROJECT}",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.7",
    install_requires=Path("requirements.txt").read_text("utf-8").split(),
    keywords=[
        PROJECT,
        "ic",
        "utils",
        "kit",
        "linux",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
    ],
)
