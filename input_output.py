"""
Module for dealing with IO related tasks.
Has methods for reading and writing CSVs.
"""

from typing import List
import csv
import sys

# Reads CSV files (including headers)
def read_csv(path: str) -> List[str]:
    """
    Reads a csv file located at path, and returns a list of items.
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
                for row in reader:
                    lines.append(row)
            except csv.Error as e:
                sys.exit(f'Error reading line {reader.line_num} from file at {path}:\n{e}')
    except Exception as err:
        sys.exit(f'Something went wrong during CSV reading.\n{err}')
    return lines


def write_csv(path, links):
    """
    Writes the output to a file using the python csv writer.
    """
    try:
        fieldnames = ["id", "links"]
        with open(path, 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
            writer.writerow(fieldnames)
            writer.writerows([k, ','.join(v)] for (k , v) in links.items())
    except Exception as err:
        sys.exit(f'Something went wrong during CSV writing.\n{err}')