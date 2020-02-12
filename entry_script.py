#!/usr/bin/env python3
from helpers import retrieve_match_type, preprocess, retrieve_master_vocab, get_vector_representation, compute_similarity_matrix, get_linked_requirements
from input_output import write_csv

if __name__ == "__main__":
    """
    Entry point for the script.

    Input:
        match_type: the type of matching to be done by the tool.
    Output:
        terminal: Some helpful messages on the usage of the program.
        files: a `links.csv` file in `/output` containing the links found, based on the match_type.
    """
    # Retrieve current match type
    match_type, match_type_explanation = retrieve_match_type()

    # Read in high and low level requirements from CSV
    low_csv_in = r'/input/low.csv'       # CSV file containing low level requirements.
    high_csv_in = r'/input/high.csv'     # CSV file containing high level requirements.

    # Preprocess the CSV file
    low_level = preprocess(low_csv_in)   # dict({id : [word, word, ...]})
    high_level = preprocess(high_csv_in) # dict({id : [word, word, ...]})

    # Retrieve the master vocabulary
    master_vocab = set(retrieve_master_vocab(low_level, high_level))
    
    # Create requirements dictionary
    requirements = {**low_level, **high_level} # Python 3.5+ syntax for joining dictionaries properly.

    # Create vector representation for requirements
    vectors = get_vector_representation(master_vocab, requirements)

    # Compute similarity matrix
    similarity = compute_similarity_matrix(high_level, low_level, vectors)

    # Link requirements based on match_type
    linked_requirements = get_linked_requirements(match_type, similarity, high_level, low_level)

    # Write linked requirements to output file
    links_output = r'/output/links.csv'  # CSV file that will contain the outputted links
    write_csv(links_output, linked_requirements)