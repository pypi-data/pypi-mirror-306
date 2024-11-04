"""This module contains the running script for the Available Nerdfonts program.

This program can be run with `python main.py` and all output will go to standard out.
Additional information can be found using `python main.py -h`.
"""

import argparse
import logging
from pprint import pprint

from src import get_download_page, parse_html


def main():
    """Main driver for the Available Nerdfonts program."""
    parser = argparse.ArgumentParser(
        prog="Available Nerdfonts",
        description="Python script to get the available Nerdfonts",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        dest="logging_level",
        const=logging.INFO,
        help="Output verbose info logs to console.",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="logging_level",
        const=logging.DEBUG,
        help="Output all program debug logs to console.",
    )

    parser.add_argument(
        "--no-output",
        action="store_false",
        dest="output",
        help="Use this flag to remove ending output, useful for viewing logs.",
    )

    args = parser.parse_args()
    logging.basicConfig(level=args.logging_level)
    nerdfonts = parse_html(get_download_page())

    if args.output:
        pprint(nerdfonts)


if __name__ == "__main__":
    main()
