from importlib.metadata import version as _version

try:
    __version__ = _version("virtualize_nex_gddp_cmip6")
except Exception:
    # Local copy or not installed with setuptools.
    # Disable minimum version checks on downstream libraries.
    __version__ = "9999"
