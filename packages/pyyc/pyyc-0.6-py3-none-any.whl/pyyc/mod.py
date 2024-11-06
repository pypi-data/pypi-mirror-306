"""
Documentation for module `mod`.
"""

__all__ = ['version']  # limits the content of "import *"

version = "top-level module"
print(f"Initialization {__name__!r}: {version}")  # NO PRINT in a true module!

####################################################

import os, sys  # pylint: disable=wrong-import-position,multiple-imports

def addition(*args):
    r"""
    Addition function (undefined type).

    Arguments should support mutual addition:

    .. math::

       \mathrm{out} = \sum_i \mathrm{arg}_i

    :param args: parameters
    :return: python addition of args
    :raises TypeError: arguments cannot be summed together

    >>> addition(1, 2, 3)
    6
    >>> addition("abc", "def")
    'abcdef'
    >>> addition([1], [2, 3], [4, 5, 6])
    [1, 2, 3, 4, 5, 6]
    >>> addition(1, "abc")
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for +=: 'int' and 'str'
    """

    out = args[0]
    for arg in args[1:]:
        out += arg

    return out


def addition_int(*args):
    """
    Addition function for integers (includes cast to integer).

    :param int args: arguments to be casted to integer
    :return: integer addition of args
    :rtype: int
    :raise ValueError: if arguments cannot be casted to integer.

    >>> addition_int(1, 2, 3)
    6
    >>> addition_int('1', 2)
    3
    >>> addition_int("abc", "def")
    Traceback (most recent call last):
        ...
    ValueError: Arguments must cast to integer.
    """

    try:
        iargs = [ int(arg) for arg in args ]
    except ValueError as exc:
        raise ValueError("Arguments must cast to integer.") from exc

    return sum(iargs)


if sys.version_info[:2] >= (3, 10):
    from importlib.resources import files  # Python 3.10+
else:
    from importlib_resources import files  # External

PYYC_PATH = files("pyyc.config")           #: Path to pyyc configuration file.


def read_config(cfgname="default.cfg"):
    """
    Get config from configuration file.

    If the input filename does not specifically include a path, it will be
    looked for in the default :const:`PYYC_PATH` directory.

    :param str cfgname: configuration file name
    :return: configuration object
    :rtype: configparser.ConfigParser

    >>> cfg = read_config()  # doctest: +ELLIPSIS
    Reading configuration from ...
    >>> cfg['DEFAULT']['version']
    'cfg-1.0'
    """

    from configparser import ConfigParser  # pylint: disable=import-outside-toplevel

    if os.path.dirname(cfgname):   # cfgname includes a path (e.g. `./path/to/file`)
        fname = cfgname
    else:                          # use PYYC_PATH as default
        fname = PYYC_PATH.joinpath(cfgname)
    print(f"Reading configuration from {fname!s}...")

    cfg = ConfigParser()
    if not cfg.read(fname):     # It silently failed
        raise IOError(f"Could not find or parse {fname!s}")

    return cfg


def format_pkg_tree(node, max_depth=2, printout=False, depth=0):
    """
    Format the package architecture.

    :param module node: name of the top-level module
    :param int max_depth: maximum depth of recursion
    :param bool printout: print out the resulting string
    :param int depth: depth level (used for recursion)
    :return: structure as a list of strings (without newlines)
    :rtype: list

    >>> import pyyc
    >>> format_pkg_tree(pyyc, max_depth=1)  # doctest: +NORMALIZE_WHITESPACE
    ['pyyc',
     '  pyyc.config',
     '  pyyc.mod',
     '  pyyc.subpkgA',
     '  pyyc.subpkgB']
    """

    if depth > max_depth:
        return []

    s = []
    if hasattr(node, '__name__'):
        s.append('  ' * depth + node.__name__)
        for name in dir(node):
            if not name.startswith('_'):
                s.extend(format_pkg_tree(getattr(node, name),
                                         max_depth=max_depth,
                                         depth=depth + 1))

    if printout:
        print('\n'.join(s))

    return s


def greetings():
    """
    Stupid function, to illustrate tests on stdin/stdout.
    """

    name = input("What's you name? ")
    print(f"Hello, {name}!")
