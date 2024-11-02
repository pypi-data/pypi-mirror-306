"""This module contains the functions and dataclasses for scrapers."""

from .dataclasses import Entry, TitledEntry
from .funcs import (
    make_request,
    parse_request,
    parse_titled_request,
)

__all__ = [
    "Entry",
    "TitledEntry",
    "make_request",
    "parse_request",
    "parse_titled_request",
]
