import importlib.metadata

try:
    __version__ = importlib.metadata.version("snarkify-cli")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

ENV = "prod"
