"""This module contains file parsing functions for the trebuchet program.
"""

import logging
import re
from enum import Enum
from typing import Iterator, List, TextIO, Tuple, Union


class Alias(Enum):
    """This enum contains single digit number/word pairs."""

    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9


def parse_file(file: TextIO) -> Iterator[Union[Tuple[str, int], None]]:
    """Parse the provided file for valid lines.

    Parameters:
        file (TextIO): text file to be parsed.

    Yields:
        A tuple containing the initial string and the integer found
        by concatenating the first and last digit.
    """
    for line in file:
        if line is None:
            yield None

        logging.debug("Parsing %s", line.strip())
        digits = parse_line(line.strip())
        logging.debug("%s parsed from %s", digits, line.strip())

        result: int = 0
        try:
            result = int(str(digits[0]) + str(digits[-1]))
        except IndexError:
            logging.debug("Returning None")
            logging.exception("%s raised exception", line.strip())
            yield None

        logging.debug("%s returned", result)
        yield (line.strip(), result)


def parse_line(line: str) -> List[int]:
    """Parse the provided string for integers.

    Parameters:
        line (str): The string to parse.

    Returns:
        A list containing all integers found.
    """
    line = "".join(_word_to_digit(list(line)))
    return [int(num) for num in re.findall(r"\d", line)]


def _word_to_digit(line: List[str]) -> List[str]:
    """Convert words in a string to digits.

    Parameters:
        line (List[str]): The string to edit.

    Returns:
        An updated list with the digits replacing
        the numerical words.
    """
    for numbers in Alias:
        has_elem = True
        while has_elem:
            rgx = re.search(str(numbers.name).lower(), "".join(line))
            if rgx is not None:
                line.insert(rgx.span()[0] + 1, str(numbers.value))
                logging.debug("Updated String: %s", "".join(line))
            else:
                has_elem = False

    return line
