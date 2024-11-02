"""This module defines the information structure for each entry containing a title."""

from dataclasses import dataclass

from .entry import Entry


@dataclass(frozen=True)
class TitledEntry(Entry):
    """Represents a chart entry for a given entry requiring a title.

    Args:
        rank: The integer rank of the entry.
        artist: A string representing the artist(s) of the entry.
        last_week_rank: The string rank this entry had last week.
        peak_rank: The highest string rank this entry has had.
        weeks_on_chart: The string number of weeks this entry has been on the chart.
        title: The string title of the entry.
    """

    title: str
