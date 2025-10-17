from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("lola")
except PackageNotFoundError:
    __version__ = "unknown"
