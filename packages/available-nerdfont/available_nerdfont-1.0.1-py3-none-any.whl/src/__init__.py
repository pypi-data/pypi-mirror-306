"""This module contains the scraper for the NerdFonts website.
"""

from .parsing import parse_html
from .scraping import get_download_page

__all__ = [
    "get_download_page",
    "parse_html",
]
