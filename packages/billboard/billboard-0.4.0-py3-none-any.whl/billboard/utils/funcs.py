"""This module contains utility functions for song charts.

Attributes:
    URL: The root URL used for all charts to append to.
    RESULT_CONTAINER: The section containing a chart entry details.
    RANKING: The containiner containing the rank of the entry.
    DETAILS_CLASS: The container containing all details of the entry.
"""

from typing import List, Optional, Union

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # type: ignore

from .dataclasses import Entry, TitledEntry

URL: str = "https://www.billboard.com/charts"
RESULT_CONTAINER = "o-chart-results-list-row-container"
RANKING = (
    "c-label a-font-primary-bold-l u-font-size-32@tablet u-letter-spacing-0080@tablet"
)
DETAILS_CLASS = "lrv-u-width-100p"


def make_request(
    chart: str, date: str, timeout: Optional[int] = 5
) -> requests.Response:
    """Make the HTTP request of the Billboard site for a specific chart.

    Args:
        chart:The chart to request (hot-100 or billboard-global-200).
        date: The date of the chart to gather.
        timeout: An optional integer to specify the timeout for making the request.

    Returns:
        The response object from the HTTP GET request.

    Raises:
        HTTPError: On a non-successful status code being returned.
    """
    ua = UserAgent()
    header = {"User-Agent": str(ua.random)}
    response = requests.get(f"{URL}/{chart}/{date}", headers=header, timeout=timeout)
    response.raise_for_status()
    return response


def parse_titled_request(response: requests.Response) -> List[TitledEntry]:
    """Parse the HTTP response for chart data with a title.

    Args:
        response: The HTTP response returned from a Billboard chart.

    Returns:
        Collection containing each chart entry.
    """
    data: List = []

    soup = BeautifulSoup(response.text, "html.parser")
    for block in soup.find_all("div", {"class": RESULT_CONTAINER}):
        data.append(_parse_titled_block(str(block)))
    return data


def _parse_titled_block(text: str) -> TitledEntry:
    soup = BeautifulSoup(text, "html.parser")
    data: List = []

    data.append(_get_ranking(soup))
    data.extend(_get_dets(soup, "title"))

    return TitledEntry(
        rank=data[0],
        title=data[1],
        artist=data[2],
        last_week_rank=data[3],
        peak_rank=data[4],
        weeks_on_chart=data[5],
    )


def parse_request(response: requests.Response) -> List[Entry]:
    """Parse the HTTP response for chart data without a title.

    Args:
        response: The HTTP response generated from the Billboard Hot 100 site.

    Returns:
        Collection containing each chart entry.
    """
    data: List = []

    soup = BeautifulSoup(response.text, "html.parser")
    for block in soup.find_all("div", {"class": RESULT_CONTAINER}):
        data.append(_parse_block(str(block)))
    return data


def _parse_block(text: str) -> Entry:
    soup = BeautifulSoup(text, "html.parser")
    data: List = []

    data.append(_get_ranking(soup))
    data.extend(_get_dets(soup, "entry"))

    return Entry(
        rank=data[0],
        artist=data[1],
        last_week_rank=data[2],
        peak_rank=data[3],
        weeks_on_chart=data[4],
    )


def _get_ranking(soup: BeautifulSoup) -> Union[int, None]:
    if (rank_html := soup.find("span", {"class": RANKING})) is not None:
        return int(rank_html.get_text(strip=True))
    return None


def _get_dets(soup: BeautifulSoup, entry: str) -> List[Union[str, None]]:
    data: List[Union[str, None]] = []
    if (details_str := soup.find("li", {"class": DETAILS_CLASS})) is not None:
        details = details_str.get_text(separator="\\", strip=True).split("\\")

        if entry == "entry":
            data.extend(details[0:1])
            data.extend(details[-3:])
        elif entry == "title":
            data.extend(details[0:2])
            data.extend(details[-3:])
    else:
        data.extend([None for _ in range(5)])
    return data
