#!/usr/bin/env python

"""The setup script."""

import io
import os
from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

cwd = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(cwd, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Darren Wiens",
    author_email="dkwiens@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="stac-nb exposes STAC in Jupyter Notebooks",
    install_requires=install_requires,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="stac_nb",
    name="stac_nb",
    packages=find_packages(include=["stac_nb", "stac_nb.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/darrenwiens/stac-nb",
    project_urls={
        "Documentation": "https://stac-nb.readthedocs.io",
        "Source": "https://github.com/darrenwiens/stac-nb",
        "Tracker": "https://github.com/darrenwiens/stac-nb/issues",
    },
    version="0.3.0",
    zip_safe=False,
)
