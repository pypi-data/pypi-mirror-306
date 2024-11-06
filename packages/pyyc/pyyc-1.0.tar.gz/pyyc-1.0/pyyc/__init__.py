"""
Documentation for package `pyyc`.
"""

__version__ = "1.0"             #: Top-level version, to be updated regularly
# NO PRINT in standard __init__.py, these one is only for educational purpose!
print(f"Initialization {__package__} v{__version__}")

from . import mod               # top-level module
from . import subpkgA           # sub-package A
from . import subpkgB           # sub-package B
