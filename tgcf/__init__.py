"""Package tgcf.

The ultimate tool to automate custom telegram message forwarding.
https://github.com/aahnik/tgcf
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(__package__)
except PackageNotFoundError:
    # Fallback for development/editable installs where metadata might not be available
    __version__ = "1.1.8"  # Should match version in pyproject.toml
