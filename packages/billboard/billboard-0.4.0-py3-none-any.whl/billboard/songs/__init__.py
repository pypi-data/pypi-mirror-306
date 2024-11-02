"""This module contains scrapers for the song-based charts on the Billboard site.

Usage Examples:
.. code-block:: python
    hot_chart = BillboardChart(YYYY-MM-DD)
    print(hot_chart.chart)

.. code-block:: python
    global_chart = GlobalChart(YYYY-MM-DD)
    print(global_chart.chart)

.. code-block:: python
    song_charts = SongCharts(YYYY-MM-DD)
    print(song_charts.hot_chart)
    print(song_charts.global_chart)
"""

from .glob import GlobalChart
from .hot import BillboardChart
from .song_charts import SongCharts

__all__ = [
    "BillboardChart",
    "GlobalChart",
    "SongCharts",
]
