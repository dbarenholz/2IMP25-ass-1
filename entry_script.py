#!/usr/bin/env python3
from helpers import retrieve_match_type
from helpers import preprocess
from helpers import retrieve_master_vocab
from helpers import get_vector_representation
from helpers import compute_similarity_matrix
from helpers import get_linked_requirements
from input_output import write_csv

if __name__ == "__main__":
    """
    Entry point for the script.

    Input:
        None.
    Output:
        None.

    TODO: Update `__main__` documentation.
    """
    # Retrieve current match type
    match_type, match_type_explanation = retrieve_match_type()

    # Read in high and low level requirements from CSV
    low_csv_in = r'/input/low.csv'
    high_csv_in = r'/input/high.csv'

    # Preprocess the CSV file
    low_level = preprocess(low_csv_in)   # dict({id : [word, word]})
    high_level = preprocess(high_csv_in) # dict({id : [word, word]})

    # Retrieve the master vocabulary
    master_vocab = set(retrieve_master_vocab(low_level, high_level))
    
    # Create requirements dictionary
    requirements = {**low_level, **high_level}

    # Create vector representation for requirements
    vectors = get_vector_representation(master_vocab, requirements)

    # Compute similarity matrix
    similarity = compute_similarity_matrix(high_level, low_level, vectors)

    # Link requirements based on match_type
    linked_requirements = get_linked_requirements(match_type, similarity, high_level, low_level)

    # Write linked requirements to output file
    links_output = r'/output/links.csv'
    write_csv(links_output, linked_requirements)