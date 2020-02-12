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


# TODO: Write this function.
def write_csv():
    """
    Writes the output to a file using the python csv writer.
    """
    pass
    # # Dummy code from template repository.
    # with open('/output/links.csv', 'w') as csvfile:
    #     writer = csv.writer(csvfile, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
    #     fieldnames = ["id", "links"]
    #     writer.writerow(fieldnames)
    #     writer.writerow(["UC1", "L1, L34, L5"]) 
    #     writer.writerow(["UC2", "L5, L4"]) 