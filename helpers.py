from typing import Tuple

from preprocessing import *

import sys

# TODO @ Jens: Check if you agree with how I do this.
def retrieve_match_type() -> Tuple[int, str]:
    """ 
    Retrieves match type from system arguments
    """

    # Dictionary.
    match_type_dict = {
        0: "No filtering.",
        1: "Similarity of at least .25.",
        2: "Similarity of at least .67 of the most similar low level requirement.",
        3: "Your own custom technique."
    }

    # Check if we have an argument.
    if len(sys.argv) < 2:
        # No argument: Print error line and exit.
        print("Please provide an argument to indicate which matcher should be used")
        exit(1)

    # Attempt to parse argument if present
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

# Perform pre processing steps for sentences
def preprocess(sentences: List[str]) -> List[List[str]]:
    # Tokenise
    tokenised = tokenize(sentences)
    
    # Filter out stop words
    filtered = remove_stop_words(tokenised)
    
    # Stem remaining words
    stemmed = stem(filtered)
    
    # Return
    return stemmed

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