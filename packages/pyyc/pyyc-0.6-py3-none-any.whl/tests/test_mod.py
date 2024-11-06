"""
Tests of :mod:`pyyc.mod` functions, to be run with :pypi:`pytest`::

  $ pytest -v test_mod.py

Ideally, each function and use case should be tested: standard use (as
described in documentation), invalid use (handled with documented exceptions),
corner cases, etc.

* :doc:`@pytest.mark.parametrize <pytest:how-to/parametrize>` decorator allows
  to test different inputs/outputs;
* :doc:`capsys <pytest:how-to/capture-stdout-stderr>` captures standard
  and error outputs (e.g. from :func:`print`);
* :doc:`monkeypatch <pytest:how-to/monkeypatch>` overrides modules and
  environments (e.g. :func:`input`).

.. Note:: Some tiny parts of the code are voluntarily left untested to
          be used as example in `coverage report`.
"""

import pytest
import pyyc

def test_version():
    """
    Simple test.
    """

    assert pyyc.mod.version == "top-level module"

@pytest.mark.parametrize("test_input, expected_output",
                         [
                             # Test on int args
                             ([1], 1), ([1, 2], 3), ([1, 2, 3], 6),
                             # Test on str args
                             (['abc',], 'abc'), (['abc', 'def'], 'abcdef'),
                             # Test on list args
                             ([[1, 2]], [1, 2]), ([[1, 2], [3, 4]], [1, 2, 3, 4]),
                          ])
def test_addition(test_input, expected_output):
    """
    Test standard usage of :func:`pyyc.mod.addition`.

    This test uses parametrization of arguments, see
    :doc:`pytest:how-to/parametrize`.

    .. Tip:: `addition(*args)` will unpack the arguments on-the-fly and
       is similar to `addition(args[0], args[1], ...)`.
    """

    assert pyyc.mod.addition(*test_input) == expected_output

@pytest.mark.parametrize("test_input", [(1, "toto"), ("toto", 1)])
def test_addition_TypeError(test_input):
    """
    Test incompatible argument case.

    It should raise :exc:`TypeError`, as mentioned in documentation of
    :func:`pyyc.mod.addition`.
    """

    with pytest.raises(TypeError):
        pyyc.mod.addition(*test_input)

def test_addition_empty():
    """
    Test no argument case.

    It should raise :exc:`IndexError`, not documented.
    """

    with pytest.raises(IndexError):
        pyyc.mod.addition()

@pytest.mark.parametrize("test_input, expected_output",
                         [([1], 1), ([1.2, 2.3], 3), ([1, 2, 3], 6)])
def test_addition_int(test_input, expected_output):
    """
    Test standard usage of :func:`pyyc.mod.addition_int`.
    """

    assert pyyc.mod.addition_int(*test_input) == expected_output

@pytest.mark.parametrize("test_input", [['1.2'], ["abc"]])
def test_addition_int_ValueError(test_input):
    """
    Test non-int argument case.

    It should raise :exc:`ValueError`, as mentioned in documentation of
    :func:`pyyc.mod.addition_int`.
    """

    with pytest.raises(ValueError):
        pyyc.mod.addition_int(*test_input)

def test_read_config_version():
    """
    Test a single value in configuration file.
    """

    cfg = pyyc.mod.read_config()
    assert cfg['DEFAULT']['version'] == 'cfg-1.0'

def test_read_config_content(capsys):
    """
    Test full content of configuration file.

    This test uses stdout capture, see :doc:`pytest:how-to/capture-stdout-stderr`.
    """

    import sys

    cfg = pyyc.mod.read_config()
    captured = capsys.readouterr()  # Capture standard & error outputs (not used)
    cfg.write(sys.stdout)           # Write config to stdout
    captured = capsys.readouterr()  # Capture standard & error outputs
    assert captured.out == "[DEFAULT]\nversion = cfg-1.0\n\n"

def test_read_config_filename():
    """
    Test explicit configuration filename.
    """

    cfg = pyyc.mod.read_config(pyyc.mod.PYYC_PATH.joinpath("default.cfg"))
    assert cfg['DEFAULT']['version'] == 'cfg-1.0'

def test_read_config_IOError():
    """
    Test non-existing or invalid configuration files.
    """

    with pytest.raises(IOError):
        pyyc.mod.read_config("nonexisting.cfg")  # Non-existing file

def test_format_pkg_tree():
    """
    Test standard usage of :func:`pyyc.mod.format_pkg_tree`.
    """

    s = pyyc.mod.format_pkg_tree(pyyc, max_depth=1)
    assert s == ['pyyc',
                 '  pyyc.config',
                 '  pyyc.mod',
                 '  pyyc.subpkgA',
                 '  pyyc.subpkgB']

def test_greetings(capsys, monkeypatch):
    """
    This test uses both input monkey patching and stdout capture.
    """

    import builtins

    # Create a fake 'input' function for the test
    monkeypatch.setattr(builtins, 'input', lambda _: "John")

    pyyc.mod.greetings()            # Use fake input, and print on stdout

    captured = capsys.readouterr()  # Capture standard & error outputs
    assert captured.out == "Hello, John!\n"
