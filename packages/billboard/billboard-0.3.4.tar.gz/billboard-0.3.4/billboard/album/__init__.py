"""This module contains scrapers for the album-based charts on Billboard.

Usage Example:
.. code-block:: python
    album_charts = AlbumChart(YYYY-MM-DD)
    print(album_charts.chart)
"""

from .album import AlbumChart

__all__ = [
    "AlbumChart",
]
