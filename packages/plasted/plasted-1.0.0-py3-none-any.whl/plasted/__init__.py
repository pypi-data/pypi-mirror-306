"""
Load an application using the environement variable `PLASTER_URI`.
"""

import importlib.metadata
import os
from typing import Any, Union

import plaster

WSGIApp = Any
__version__ = importlib.metadata.version("plasted")


def load_app(plaster_uri: Union[str, None]) -> WSGIApp:
    if plaster_uri is None:
        raise LookupError("missing environment variable PLASTER_URI")

    loader = plaster.get_loader(plaster_uri)
    loader.setup_logging({})
    return loader.get_wsgi_app()


app = load_app(os.getenv("PLASTER_URI"))
