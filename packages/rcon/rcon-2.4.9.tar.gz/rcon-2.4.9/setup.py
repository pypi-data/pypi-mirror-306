#! /usr/bin/env python
"""Installation script."""

from setuptools import setup

setup(
    name="rcon",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="Richard Neumann",
    author_email="mail@richard-neumann.de",
    python_requires=">=3.10",
    packages=["rcon", "rcon.battleye", "rcon.source"],
    extras_require={"GUI": ["pygobject", "pygtk"]},
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "rcongui = rcon.gui:main",
            "rconclt = rcon.rconclt:main",
            "rconshell = rcon.rconshell:main",
        ],
    },
    url="https://github.com/conqp/rcon",
    license="GPLv3",
    description="An RCON client library.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="python rcon client",
)
