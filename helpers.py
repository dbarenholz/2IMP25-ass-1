from typing import Tuple

from preprocessing import *

import sys

# Retrieves match type from system arguments
def retrieve_match_type() -> Tuple[int, str]:
    """ 
    Retrieves match type from system arguments
    """

    # Dictionary relating integer with type of matching to be used.
    match_type_dict = {
        0: "No filtering.",
        1: "Similarity of at least .25.",
        2: "Similarity of at least .67 of the most similar low level requirement.",
        3: "Your own custom technique."
    }

    # Check if we have an(y) argument(s).
    if len(sys.argv) < 2:
        # No argument(s): Print error line and exit.
        print("Please provide an argument to indicate which matcher should be used")
        exit(1)

    # Attempt to parse argument(s) if present
    match_type = 0
    try:
        match_type = int(sys.argv[1])
    except ValueError:
        # Problem parsing argument as number
        print("Match type provided is not a valid number")
        exit(1)
    
    # We have a match_type!
    print(f"Using match type {match_type}: {match_type_dict[match_type]}")
    return match_type, match_type_dict[match_type]

# Reads CSV files (including headers)
def read_csv(path: str) -> List[str]:
    """
    Reads a csv file located at path, and returns a list of items.
    Exits on errors.
    """
    import csv

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

# Perform pre processing steps for sentences
def preprocess(csv: str) -> List[List[str]]:
    """
    Preprocesses a csv for use in the program.
    
    See also:
        `stem()`
        `remove_stop_words()`
        `tokenize()`
    """
    # Download necessary nltk resources
    from nltk import download
    download('punkt')

    # Dictionary comprehension on result from read_csv
    d = {r_id: text for (r_id, text) in read_csv(csv)[1:]}

    # Perform necessary preprocessing steps on each requirement
    for r_id, text in d.items():
        d[r_id] = stem(remove_stop_words(tokenize(text)))

    return d

# TODO: Write this function.
def write_output_file():
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