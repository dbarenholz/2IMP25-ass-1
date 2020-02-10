#!/usr/bin/env python3
from helpers import retrieve_match_type
from helpers import preprocess

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
    
    # Preprocess the CSV file
    low_level = preprocess(low_csv_in)
    
    # high_csv_in = r'/input/high.csv'
    # high_level = read_csv(high_csv_in)


    # write_output_file()