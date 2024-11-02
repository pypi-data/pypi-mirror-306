"""This module contains the parent class for all song chart classes."""

from abc import abstractmethod
from typing import List

from billboard.super import Chart
from billboard.utils import TitledEntry as SongEntry


class SongChart(Chart):
    """Abstract class containing song charts interface.

    Attributes:
        date: The date for this chart in ISO 8601 format (YYYY-MM-DD).
        chart: The chart for the given date containing all chart data.
        auto_date: Determines if the object will auto update the date to the
            previous week if the chosen one does not exist.
        oldest_date: The oldest date allowed for a given chart.
    """

    @property
    def top_spot(self) -> SongEntry:
        """Get the top spot from this week.

        Returns:
            A data structure containing the top spot information.
        """
        return self.chart[0]

    def artist_entries(self, artist: str, rank: int = 100) -> List[SongEntry]:
        """Get the entries an artist has on this chart.

        Args:
            artist: The artists name.
        rank: An optional variable for specifying an end value on ranking.

        Returns:
            A List containing all entries this artist has.
        """
        return [
            entry
            for entry in self.chart
            if entry.artist.lower() == artist.lower() and entry.rank <= rank
        ]

    @abstractmethod
    def _generate_chart(self):
        """Generate the chart for the given week."""
        raise NotImplementedError  # pragma: no cover
