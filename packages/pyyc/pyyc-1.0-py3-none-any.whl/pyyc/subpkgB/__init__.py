"""
Documentation for sub-package `subpkgB`.
"""

version = 'sub-package B'
print(f"Initialization {__package__!r}: {version}")

from .modB import *  # local import of elements in `mod.__all__`
