"""Configuration."""

from importlib.metadata import metadata

meta = metadata("ngs-test-utils")

# General information about the project.
project = "NGS test utils"
version = meta["version"]
release = version
author = meta["author"]
copyright = "2024, " + author
