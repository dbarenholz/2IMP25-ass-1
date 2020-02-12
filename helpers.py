"""
Module for helper functions specific to the assignment.

"""

from typing import Tuple, Dict, Set
from preprocessing import *
from input_output import read_csv
import sys
import numpy as np

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
    except ValueError as e:
        # Problem parsing argument as number
        print("Match type provided is not a valid number")
        print(e)
        exit(1)
    
    # We have a match_type!
    print(f"Using match type {match_type}: {match_type_dict[match_type]}")
    return match_type, match_type_dict[match_type]

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

# Creates vocabulary list given various dictionaries
def retrieve_master_vocab(*args: Dict[str, List[str]]) -> List[str]:
    """
    Given any number of dictionaries of following form:
    {
        key : [token1, token2, ...]
    }
    Returns a flattened list of all tokens.
    """
    # Create empty list
    tokens = []

    # For each dictionary
    for d in args:
        # Extend the token list with all values
        for item in d.values():
            tokens.extend(item)
    # Return a complete list of tokens
    return tokens

# Private method to precompute d
def __precompute_d(vocabulary: Set[str], requirements: Dict[str, List[str]]) -> Dict[str, int]:
    """
    Computes d according to the provided scheme.
    """
    d = {k : v for k, v in zip(vocabulary, len(vocabulary)*[0])}

    for requirement in requirements.values():
        for token in vocabulary:
            if token in requirement:
                d[token] = d[token] + 1

    return d

def __update_vector_repr(vocabulary: Set[str], requirements: Dict[str, List[str]], d: Dict[str, int]) -> Dict[str, List[float]]:
    """
    TODO
    """
    # For each item in the created dictionary (with wrong values)
    for (req_id, req_tokens) in requirements.items():
        # Create a list for the correct values
        req_vec = []

        # Loop over the master vocabulary
        for token in vocabulary:
            # Check if the token is in the requirement itself (req_tokens)
            if token not in req_tokens:
                # If the token is not in the requirement: w_i = 0
                req_vec.append(0)
            else:
                # If the token IS in the requirement: w_i = tf * idf
                
                # frequency of ith word (=token) of master vocab in r (=req_tokens)
                tf = req_tokens.count(token)

                # log_2 (n / d) 
                idf = np.log2( float(len(requirements)) / d[token])

                req_vec.append(tf * idf)
        # Update vector representation with correct values
        requirements[req_id] = req_vec
    return requirements

def get_vector_representation(vocabulary: Set[str], requirements: Dict[str, List[str]]) -> Dict[str, List[float]]:
    """
    TODO
    """
    d = __precompute_d(vocabulary, requirements)
    return __update_vector_repr(vocabulary, requirements, d)

def get_cosine_similarity(a, b):
    return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))

def compute_similarity_matrix(high_level, low_level, vectors):
    matrix = np.zeros((len(high_level), len(low_level)), dtype=np.float64)

    rows = matrix.shape[0] # ignore vscode error
    cols = matrix.shape[1] # ignore vscode error

    for i in range(0, rows):
        for j in range(0, cols):
            hkey = list(high_level.keys()) [i]
            lkey = list(low_level.keys()) [j]
            matrix[i, j] = get_cosine_similarity(vectors[hkey], vectors[lkey])

    return matrix

def get_linked_requirements(match_type, similarity, high_level, low_level):
    # Create links structure
    links = {hkey: [] for hkey in high_level.keys()}
    if match_type == 0:
        # no filtering: similarity > 0 --> link reqs

        rows = similarity.shape[0] # ignore vscode error
        cols = similarity.shape[1] # ignore vscode error

        for i in range(0, rows):
            for j in range(0, cols):
                hkey = list(high_level.keys()) [i]
                lkey = list(low_level.keys()) [j]
                if similarity[i, j] > 0:
                    print(f"hkey: {hkey}")
                    print(f"lkey: {lkey}")
                    links[hkey].append(lkey)
                    print(f"Added: {links[hkey]}")


    elif match_type == 1:
        # similarity > 0.25 --> link reqs
        rows = similarity.shape[0] # ignore vscode error
        cols = similarity.shape[1] # ignore vscode error

        for i in range(0, rows):
            for j in range(0, cols):
                hkey = list(high_level.keys()) [i]
                lkey = list(low_level.keys()) [j]
                if similarity[i, j] > 0.25:
                    links[hkey].append(lkey)
    elif match_type == 2: 
        # similarity > (0.67 * highest similarity) per high_level requirement --> link reqs
        rows = similarity.shape[0] # ignore vscode error
        cols = similarity.shape[1] # ignore vscode error

        for i in range(0, rows):

            max_similarity = max(similarity[i])

            for j in range(0, cols):
                hkey = list(high_level.keys()) [i]
                lkey = list(low_level.keys()) [j]
                if similarity[i, j] > 0.67 * max_similarity:
                    links[hkey].append(lkey)

    elif match_type == 3:
        rows = similarity.shape[0] # ignore vscode error
        # custom choice
        for i in range(0, rows):
            hkey = list(high_level.keys()) [i]
            links[hkey].append("todo")

    return links