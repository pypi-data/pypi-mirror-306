"""This module contains the interface to be used by all other scrapers."""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional


class Chart(ABC):
    """Abstract class containing charts interface.

    Attributes:
        date: The date for this chart in ISO 8601 format (YYYY-MM-DD).
        chart: Structure containing all chart data.
        auto_date: Determines if the object will auto update the date to the
            previous week if the chosen one does not exist.
        oldest_date: The oldest date allowed for a given chart.
    """

    def __init__(
        self,
        date: Optional[str] = None,
        auto_date: bool = True,
        oldest_date: str = "1958-08-04",
    ) -> None:
        """The constructor for a Chart object.

        Args:
            date: An optional date (YYYY-MM-DD); if none is provided, yesterday is used.
            auto_date: Determines if the object will auto update the date to the
                previous week if the choosen one does not exist.
            oldest_date: Set the oldest date allowed for a given chart.
        """
        self.chart: List = []
        self.auto_date = auto_date
        self.oldest_date = oldest_date
        if date is not None:
            self.date = date
        else:
            self.date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    @property
    def date(self) -> str:
        """Get the data used for the current chart.

        Returns:
            The ISO 8601 formatted date.
        """
        return self._date

    @date.setter
    def date(self, iso_date: str) -> None:
        """Set a new date for the class and update the current chart.

        Args:
            iso_date: The ISO 8601 string.

        Raises:
            ValueError: If the date is not in YYYY-MM-DD format.
        """
        try:
            date = datetime.fromisoformat(iso_date)
        except ValueError as e:
            raise e

        if date < datetime.fromisoformat(self.oldest_date) or date > datetime.today():
            raise ValueError("Invalid date provided")

        self._date = date.strftime("%Y-%m-%d")
        self._generate_chart()

    @abstractmethod
    def _generate_chart(self):
        """Generate the chart for the given week."""
        raise NotImplementedError  # pragma: no cover
