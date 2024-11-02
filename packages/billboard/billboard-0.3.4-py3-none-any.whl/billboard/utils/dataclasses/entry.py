"""This module defines the information structure for each entry."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Entry:
    """Represents a chart entry.

    Args:
        rank: The integer rank of the entry.
        artist: A string representing the artist(s) of the entry.
        last_week_rank: The string rank this entry had last week.
        peak_rank: The highest string rank this entry has had.
        weeks_on_chart: The string number of weeks this entry has been on the chart.
    """

    rank: int
    artist: str
    last_week_rank: str
    peak_rank: str
    weeks_on_chart: str
