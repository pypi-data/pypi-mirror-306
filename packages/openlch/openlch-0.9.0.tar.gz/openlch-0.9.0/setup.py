# mypy: disable-error-code="import-untyped"
#!/usr/bin/env python
"""Setup script for the project."""

import re

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description: str = f.read()


with open("openlch/requirements.txt", "r", encoding="utf-8") as f:
    requirements: list[str] = f.read().splitlines()


with open("openlch/requirements-dev.txt", "r", encoding="utf-8") as f:
    requirements_dev: list[str] = f.read().splitlines()


with open("openlch/__init__.py", "r", encoding="utf-8") as fh:
    version_re = re.search(r"^__version__ = \"([^\"]*)\"", fh.read(), re.MULTILINE)
assert version_re is not None, "Could not find version in openlch/__init__.py"
version: str = version_re.group(1)


setup(
    name="openlch",
    version=version,
    description="The OpenLCH project command line interface",
    author="OpenLCH Contributors",
    url="https://github.com/Zeroth-Robotics/openlch-client-py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    install_requires=requirements,
    tests_require=requirements_dev,
    extras_require={"dev": requirements_dev},
    packages=["openlch"],
    entry_points={
        "console_scripts": [
            "openlch=openlch.cli:cli",
        ],
    },
)
