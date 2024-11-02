"""This module contains a bundled class containing both the Hot 100
and Global 200 scrapers.
"""

from typing import List, Optional

from billboard.songs import BillboardChart, GlobalChart
from billboard.utils import TitledEntry as SongEntry


class SongCharts:
    """Class to manage all song charts available.

    Attributes:
        date (str): The date for the charts in ISO 8601 format (YYYY-MM-DD)
        hot100 (BillboardChart): The Hot 100 chart.
        global200 (GlobalChart): The Global 200 chart.
    """

    def __init__(self, date: Optional[str] = None) -> None:
        """The constructor for the SongCharts.

        Args:
            date: An optional date (YYYY-MM-DD); if none is provided, yesterday is used.
        """
        self.hot100 = BillboardChart(date)
        self.global200 = GlobalChart(date)

    @property
    def hot_chart(self) -> List[SongEntry]:
        """Return the Hot 100 chart.

        Returns:
            A list containing SongEntry elements.
        """
        return self.hot100.chart

    @property
    def global_chart(self) -> List[SongEntry]:
        """Return the Global 200 chart.

        Returns:
            A list containing SongEntry elements.
        """
        return self.global200.chart
