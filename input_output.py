"""
Module for dealing with IO related tasks.
Has methods for reading and writing CSVs.
"""

import csv
import sys
from typing import Dict, List


def read_csv(path: str) -> List[str]:
    """
    Reads a csv file located at path, and returns a list of lines.
    Exits on errors.
    """

    # Create lines list
    lines = []

    # Attempt to open the path
    try:
        with open(path, 'r') as f:
            # Create a default reader from the file
            reader = csv.reader(f)
            # Attempt to read each line.
            try:
                # Done on a per-line basis for proper error handling.
                for row in reader:
                    lines.append(row)
            except csv.Error as e:
                sys.exit(f'Error reading line {reader.line_num} from file at {path}:\n{e}')
    except Exception as err:
        sys.exit(f'Something went wrong during CSV reading.\n{err}')
    # Return lines from CSV file
    return lines


def write_csv(path: str, links: Dict[str, List[str]]) -> None:
    """
    Writes the output to a file using the python csv writer.
    """
    # Attempt to open the path
    try:
        with open(path, 'w') as f:
            # Create a writer with specific settings
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
            writer.writerow(["id", "links"])
            writer.writerows([k, ','.join(v)] for (k , v) in links.items())
    except Exception as err:
        sys.exit(f'Something went wrong during CSV writing.\n{err}')