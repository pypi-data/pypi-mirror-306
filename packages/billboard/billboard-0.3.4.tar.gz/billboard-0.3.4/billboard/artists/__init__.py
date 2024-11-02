"""This module contains scrapers for the artist-based charts on Billboard.

Usage Example:
.. code-block:: python
    artist_charts = ArtistChart(YYYY-MM-DD)
    print(artist_charts.chart)
"""

from .artist import ArtistChart

__all__ = [
    "ArtistChart",
]
