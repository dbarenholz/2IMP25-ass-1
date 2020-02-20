"""
Module for helper functions specific to this assignment.
Contains various methods.
"""
import sys
import numpy as np
from typing import Tuple, Dict, Set

from preprocessing import *
from input_output import read_csv


# === Private Methods === #


def __retrieve_match_type() -> Tuple[int, str]:
    """
    Retrieves match type from system arguments
    """
    # Check if we have an(y) argument(s).
    if len(sys.argv) < 2:
        # No argument(s): Print error line and exit.
        print("ERROR! retrieve_match_type(): Please provide an argument to indicate which matcher should be used")
        exit(1)

    # Attempt to parse argument(s) if present
    match_type = 0
    try:
        match_type = int(sys.argv[1])
    except ValueError as e:
        # Problem parsing argument as number
        print("ERROR! retrieve_match_type(): Match type provided is not a valid number")
        print(e)
        exit(1)

    # Check if match_type is allowed
    allowed_match_types = list(range(0, 4))
    if match_type not in allowed_match_types:
        print("WARN! retrieve_match_type(): Match type not defined. Using default type (1)")
        match_type = 1

    # We have a match_type!
    return match_type


def __precompute_d(vocabulary: Set[str], requirements: Dict[str, List[str]]) -> Dict[str, int]:
    """
    Computes d according to its formula (tf*idf) for use in computing a vector representation
    """
    d = {k : v for k, v in zip(vocabulary, len(vocabulary)*[0])}

    for requirement in requirements.values():
        for token in vocabulary:
            if token in requirement:
                d[token] = d[token] + 1

    return d


def __update_vector_repr(vocabulary: Set[str], requirements: Dict[str, List[str]], d: Dict[str, int]) -> Dict[str, List[float]]:
    """
    Converts a placeholder requirements dictionary with its actual vector representation.
    """
    # For each item in the placeholder dictionary (with wrong values)
    for (req_id, req_tokens) in requirements.items():
        # Create a list for the correct values
        req_vec = []

        # Loop over the master vocabulary
        for token in vocabulary:
            # Check if the token is in the requirement itself (req_tokens)
            if token not in req_tokens:
                # If the token IS NOT in the requirement: w_i = 0
                req_vec.append(0)
            else:
                # frequency of ith word of master vocab (=token) in r (=req_tokens)
                tf = req_tokens.count(token)

                # log_2 (n / d); casting is done just in case, to prevent integer division
                idf = np.log2(float(len(requirements)) / d[token])

                # If the token IS in the requirement: w_i = tf * idf
                req_vec.append(tf * idf)
        # Update vector representation with correct values
        requirements[req_id] = req_vec

    return requirements


def __get_cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Computes and the cosine similarity between two vectors, a and b.
    """
    return float(np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b)))


def __add_to_dict(dict: Dict[str, List[str]], key:str, value: List[str]):
    """
    Adds value to key in dictionary is value is not empty
    """
    if (len(value) != 0):
        dict[key] = value

def __compute_total_values_dict(dict: Dict[str, List[str]]) -> int:
    """
    Computes the sum of the length of all the values in the dictionary
    """
    return sum([len(list_element) for list_element in dict.values()])


# === Public Methods === #


def preprocess(csv: str) -> Dict[str, List[str]]:
    """
    Preprocesses a csv for use in the program.

    See also:
        `__stem()`
        `__remove_stop_words()`
        `__tokenize()`
    """
    # Download necessary nltk resources
    from nltk import download
    download('punkt')

    # Create dictionary for a CSV file.
    # The header row is skipped ([1:])
    d = {r_id: text for (r_id, text) in read_csv(csv)[1:]}

    # Perform necessary preprocessing steps on each requirement sentence
    for (r_id, text) in d.items():
        d[r_id] = stem(remove_stop_words(tokenize(text)))

    # Return the finalised dictionary
    return d


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


def get_vector_representation(vocabulary: Set[str], requirements: Dict[str, List[str]]) -> Dict[str, List[float]]:
    """
    Given a vocabulary and set of requirements, computes and returns its vector representation.
    """
    d = __precompute_d(vocabulary, requirements)

    return __update_vector_repr(vocabulary, requirements, d)


def compute_similarity_matrix(high_level: Dict[str, List[str]], low_level: Dict[str, List[str]], vectors: Dict[str, List[float]]) -> np.ndarray:
    """
    Computes a cosine similarity matrix between high level and low level requirements.
    """
    # Create initial matrix of size (amount high level reqs * amount low level reqs)
    matrix = np.zeros((len(high_level), len(low_level)), dtype=np.float64)

    # Loop through the created placeholder matrix, and fill it with the cosine similarity
    rows = matrix.shape[0] # pylint: disable=E1136  # pylint/issues/3139
    cols = matrix.shape[1] # pylint: disable=E1136  # pylint/issues/3139

    for i in range(0, rows):
        for j in range(0, cols):
            # Retrieve the high and low level requirements keys, needed for finding the corresponding vectors.
            hkey = list(high_level.keys()) [i]
            lkey = list(low_level.keys()) [j]
            matrix[i, j] = __get_cosine_similarity(vectors[hkey], vectors[lkey])

    # Return the computed matrix
    return matrix


def get_linked_requirements(similarity: np.ndarray, high_level: Dict[str, List[str]], low_level: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Compute and return links between requirements, based on matching type.
    """
    # Retrieve current match type
    match_type = __retrieve_match_type()

    # Dictionary relating integer with type of matching to be used.
    match_type_dict = {
        0: ["No filtering.", 0.0],
        1: ["Similarity of at least .25.", 0.25],
        2: ["Similarity of at least .67 of the most similar low level requirement.", 0.67],
        3: ["Your own custom technique.", 0.25, 0.67]
    }

    # Log the type of filtering to be used
    print(f"INFO! get_linked_requirements(): Using match type {match_type}: {match_type_dict[match_type][0]}")

    # Create links structure
    links = {hkey: [] for hkey in high_level.keys()}

    # Loop over similarity matrix
    rows = similarity.shape[0]
    cols = similarity.shape[1]

    for i in range(0, rows):
        # Compute max_similarity for match_type == 2 and match_type == 3
        max_similarity = max(similarity[i])

        for j in range(0, cols):
            # Retrieve keys for later usage
            hkey = list(high_level.keys())[i]
            lkey = list(low_level.keys())[j]

            # Add links based on match-type
            if match_type == 1:
                if similarity[i, j] >= match_type_dict[match_type][1]:
                    links[hkey].append(lkey)
            elif match_type == 2:
                if similarity[i, j] >= match_type_dict[match_type][1] * max_similarity:
                    links[hkey].append(lkey)
            elif match_type == 3:
                if (max_similarity >= match_type_dict[match_type][1] and similarity[i, j] >= match_type_dict[match_type][2] * max_similarity):
                    links[hkey].append(lkey)
            else:
                if similarity[i, j] > match_type_dict[match_type][1]:
                    links[hkey].append(lkey)

    return links


def get_links_expert(expert_path: str) -> Dict[str, List[str]]:
    """
    Reads csv and construct proper links from experts
    """
    # Create dictionary for a CSV file.
    # The header row is skipped ([1:])
    links_expert = {r_id: text for (r_id, text) in read_csv(expert_path)[1:]}

    # Fill dictionary
    for (r_id, text) in links_expert.items():
        # Create list of seperate links
        str_list = text.split(',')

        # Remove leading and trailing whitespace of all list items
        for i in range(0, len(str_list)):
            str_list[i] = str_list[i].strip()

        # Set dictionary value equal to list
        links_expert[r_id] = str_list

    # Return the resulting dictionary
    return links_expert


def get_evaluation_sets(linked_requirements: Dict[str, List[str]], links_expert: Dict[str, List[str]], low_level: Dict[str, List[str]], high_level: Dict[str, List[str]]) -> Tuple[Dict[str, List[str]], Dict[str, List[str]], Dict[str, List[str]], Dict[str, List[str]]]:
    """
    Performs evaluation on indicated and predicted links
    First is Indicated + Predicted, Second is Indicated + Not Predicted, Third is Not Indicated + Predicted, Fourth is Not Indicated + Not Predicted
    """
    # Initialize dictionaries
    idpr, idnpr, nidpr, nidnpr = {}, {}, {}, {}

    # Loop over all known high_level requirements
    for r_id in high_level.keys():
        # Calculate indicated + predicted by taking intersection of values in expert and values in calculated links
        __add_to_dict(idpr, r_id, list(filter(None, set(links_expert[r_id]).intersection(set(linked_requirements[r_id])))))

        # Calculate indicated + not predicted by removing predicted from indicated
        __add_to_dict(idnpr, r_id, list(filter(None, set(links_expert[r_id]) - set(linked_requirements[r_id]))))

        # Calculate not indicated + predicted by removing indicated from predicted
        __add_to_dict(nidpr, r_id, list(filter(None, set(linked_requirements[r_id]) - set(links_expert[r_id]))))

        # Calculate not indicated + not predicted by removing union of values in expert and values in calculted links from the set of all low level keys
        __add_to_dict(nidnpr, r_id, list(filter(None, set(low_level.keys()) - set(linked_requirements[r_id]).union(set(links_expert[r_id])))))

    # Return the 4 resulting dictionaries
    return (idpr, idnpr, nidpr, nidnpr)


def get_evaluation_counts(idpr: Dict[str, List[str]], idnpr: Dict[str, List[str]], nidpr: Dict[str, List[str]], nidnpr: Dict[str, List[str]], high_level: Dict[str, List[str]]) -> Tuple[int, int, int, int]:
    """
    Computes counts of the dictionary used in evaluation
    """
    # Return the 4 resulting counts
    return (__compute_total_values_dict(idpr), __compute_total_values_dict(idnpr), __compute_total_values_dict(nidpr), __compute_total_values_dict(nidnpr))