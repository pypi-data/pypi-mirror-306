"""This module contains the scraper for the Artist 100 chart."""

from datetime import datetime, timedelta
from typing import Optional

from billboard.super import Chart
from billboard.utils import Entry as ArtistEntry
from billboard.utils import make_request, parse_request


class ArtistChart(Chart):
    """
    A data structure representing a week of the Artist 100 Billboard Chart.

    Attributes:
        date: The date for this chart in ISO 8601 format (YYYY-MM-DD).
        chart: The chart for the given date containing all chart data.
        auto_date: Determines if the object will auto update the date to the
            previous week if the chosen one does not exist.
        oldest_date: The oldest date allowed for a given chart.
    """

    def __init__(self, date: Optional[str] = None, auto_date: bool = True) -> None:
        """The constructor for a ArtistChart object.

        Args:
            date: An optional date (YYYY-MM-DD); if none is provided, yesterday is used.
            auto_date: Determines if the object will auto update the date to the
                previous week if the choosen one does not exist.
        """
        super().__init__(date, auto_date, "2014-07-19")

    @property
    def top_spot(self) -> ArtistEntry:
        """Get the top spot from this week.

        Returns:
            A data structure containing the top spot information.
        """
        return self.chart[0]

    def _generate_chart(self):
        """Generate the chart for the given week."""
        response = make_request("artist-100", self.date)
        if (data := parse_request(response)) == [] and self.auto_date is True:
            week_ago = datetime.fromisoformat(self.date) - timedelta(weeks=1)
            self.date = week_ago.strftime("%Y-%m-%d")
        else:
            self.chart = data
