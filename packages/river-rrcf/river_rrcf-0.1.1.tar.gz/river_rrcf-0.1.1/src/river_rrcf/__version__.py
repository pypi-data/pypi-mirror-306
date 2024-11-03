from importlib.metadata import version

try:
    __version__ = version("river-rrcf")
except Exception:  # pragma: no cover
    __version__ = "unknown"
