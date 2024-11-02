"""This module contains scrapers for the Billboard music charts site.

Example Usage:
.. code-block:: python
    from billboard import CHART_TYPE
    result = CHART_TYPE(YYYY-MM-DD)
    print(result.chart)

"""

from .album import AlbumChart
from .artists import ArtistChart
from .songs import BillboardChart, GlobalChart, SongCharts

__all__ = [
    "SongCharts",
    "BillboardChart",
    "GlobalChart",
    "ArtistChart",
    "AlbumChart",
]
