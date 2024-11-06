#!/usr/bin/env python3

"""The main module for the trebuchet program.
"""


import logging
from pathlib import Path

import click

from .parse import parse_file


@click.command()
@click.version_option("0.1.0", prog_name="trebuchet")
@click.argument(
    "input_file", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    default=False,
    help="Output debug logs to standard out",
)
def main(input_file, debug):
    """The main driver for the trebuchet program.

    INPUT_FILE is the file passed in to parse.
    """
    if debug is True:
        logging.basicConfig(level=logging.DEBUG)
    logging.debug("%s of type %s accepted", input_file, type(input_file))

    result = 0
    with open(input_file, "r", encoding="utf-8") as file:
        for lines in parse_file(file):
            if lines is not None:
                result += lines[1]

    print(f"The result is {result}")


if __name__ == "__main__":
    main()
