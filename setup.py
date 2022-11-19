from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "1.1.3"
DESCRIPTION = "UNOFFICIAL Python bindings for IPRoyal Pawns (Pawns.app) Dashboard API"
LONG_DESCRIPTION = "A package that allows you to connect to IPRoyal Pawns (Pawns.app) API and interact with your data."

# Setting up
setup(
    name = "pyIPRoyalPawns",
    version = VERSION,
    author = "coder-amogh (Amogh Datar)",
    description = DESCRIPTION,
    long_description_content_type = "text/markdown",
    long_description = long_description,
    packages = find_packages(),
    install_requires = ['requests', 'pySocks'],
    url = "https://github.com/coder-amogh/pyIPRoyalPawns",
    project_urls = {
        "Bug Tracker": "https://github.com/coder-amogh/pyIPRoyalPawns/issues",
    },
    keywords = ['python', 'iproyal', 'ipr', 'passive income', 'iproyal pawns api', 'iproyal pawns dashboard', "python iproyal pawns", "pawns.app"],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
