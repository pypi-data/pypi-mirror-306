"""
Documentation for module `subpkgB.modB`.
"""

from ..subpkgA import modA1  # relative import

version = f'sub-package B module (incl. {modA1.version})'
print(f"Initialization {__name__!r}: {version}")
