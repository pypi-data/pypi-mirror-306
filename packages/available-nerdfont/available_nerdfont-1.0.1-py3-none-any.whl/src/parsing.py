"""This module contains parsing functionality for the Nerdfonts
website, https://www.nerdfonts.com/
"""

import logging
from typing import List

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def parse_html(response: str) -> List[str]:
    """Parse the response HTML for Nerdfonts available

    :param response: The HTML response returned
    :type response: str
    :return List of Nerdfonts available
    :rtype: List[str]
    """
    soup = BeautifulSoup(response, "html.parser")
    collection = []
    for tag in soup.find_all("div", class_="item"):
        logging.debug("Analyzing tag %s", tag)
        for anchor in tag.find_all("a", class_="font-preview"):
            logging.debug("Parsing tag %s", anchor)
            collection.append(_parse_anchor(anchor["href"]))
    return collection


def _parse_anchor(anchor: str) -> str:
    """Parse the anchor tag for the resulting Nerdfont

    :param anchor: The anchor tag containing the information
    :type anchor: str
    :return Name of the Nerdfont
    :rtype str
    """
    result = anchor.strip(".zip").split("/")
    logging.info("Found %s Nerd Font", result[-1])
    return result[-1]
