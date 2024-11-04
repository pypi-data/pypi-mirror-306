"""This module contains functionality pertaining to the scraping of the
nerdfonts website, https://www.nerdfonts.com/
"""

from urllib.request import urlopen

DOWNLOAD_URL = "https://www.nerdfonts.com/font-downloads"


def get_download_page(timeout: int = 5) -> str:
    """
    Get the HTML content from the downloads page

    :param timeout: The timeout value to use
    :type timeout: int
    :return The HTML of the downloads page
    :rtype: str
    """
    return urlopen(DOWNLOAD_URL, timeout=timeout).read().decode("utf-8")
