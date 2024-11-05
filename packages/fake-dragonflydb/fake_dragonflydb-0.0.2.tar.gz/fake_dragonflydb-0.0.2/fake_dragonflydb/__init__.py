from ._server import (
    FakeServer,
    FakeDragonDB,
    FakeStrictDragonDB,
    FakeConnection,
)
from .async_db import (
    FakeAsyncDragonDB,
    FakeAsyncConnection,
)

try:
    from importlib import metadata
except ImportError:  # for Python < 3.8
    import importlib_metadata as metadata  # type: ignore
__version__ = metadata.version("fake-dragonflydb")
__author__ = "Daniel Moran"
__maintainer__ = "Daniel Moran"
__email__ = "daniel@moransoftware.ca"
__license__ = "BSD-3-Clause"
__url__ = "https://github.com/cunla/fakeredis-py"
__bugtrack_url__ = "https://github.com/cunla/fakeredis-py/issues"

__all__ = [
    "FakeServer",
    "FakeDragonDB",
    "FakeStrictDragonDB",
    "FakeConnection",
    "FakeAsyncDragonDB",
    "FakeAsyncConnection",
]
