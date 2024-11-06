#! /usr/bin/env python
import os
import sys

from setuptools import Extension, find_packages, setup

entry_points = {
    "pymt.plugins": [
        "FrostNumber=pymt_permamodel.bmi:FrostNumber",
        "Ku=pymt_permamodel.bmi:Ku",
        "KuEnhanced=pymt_permamodel.bmi:KuEnhanced",
    ]
}


def read(filename):
    with open(filename, "r", encoding="utf-8") as fp:
        return fp.read()


long_description = "\n\n".join(
    [read("README.rst"), read("CREDITS.rst"), read("CHANGES.rst")]
)


setup(
    name="pymt_permamodel",
    author="CSDMS",
    author_email="csdms@colorado.edu",
    description="PyMT plugin for pymt_permamodel",
    long_description=long_description,
    version="0.2.3",
    url="https://github.com/pymt-lab/pymt_permamodel",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["bmi", "pymt"],
    install_requires=open("requirements.txt", "r").read().splitlines(),
    packages=find_packages(),
    entry_points=entry_points,
    include_package_data=True,
)
