def test_import_pyblog():
    """Ensure the package imports and exposes a `__version__` string.

    This is a lightweight check to catch broken packaging or missing files.
    """
    import pyblog

    assert hasattr(pyblog, "__version__")
    assert isinstance(pyblog.__version__, str)
