#!/usr/bin/env python3
from helpers import retrieve_match_type

if __name__ == "__main__":
    """
    Entry point for the script.

    Input:
        None.
    Output:
        None.

    TODO: Update `__main__` documentation.
    """
    low_csv_in = r'/input/low.csv'
    high_csv_in = r'/input/high.csv'

    match_type, match_type_explanation = retrieve_match_type()

    
    '''
    This is where you should implement the trace level logic as discussed in the 
    assignment on Canvas. Please ensure that you take care to deliver clean,
    modular, and well-commented code.
    '''

    # write_output_file()