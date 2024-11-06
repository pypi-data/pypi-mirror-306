"""
Documentation for sub-package `subpkgA`.
"""

version = 'sub-package A'
print(f"Initialization {__package__!r}: {version}")
__all__ = ['modA1', 'modA2']  # modules imported by `import *`

for _mod in __all__:
    __import__(__name__ + '.' + _mod, fromlist=[None])  # ≈ 'from __name__ import _mod'
