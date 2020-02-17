"""
Module for preprocessing sentences.
Contains methods for tokenisation, stop-word filtering, and stemming.
"""

from typing import List
from sys import exit

# Provides tokenisation
def tokenize(sentence: str) -> List[str]:
    """
    Parses and tokenizes a set of sentences and returns a list of lists of tokens, per sentence.

    Input:
        sentence: Single requirement sentence.
    Output:
        result: List of tokens
    """
    # Check if we have a list
    if not isinstance(sentence, str):
        exit(f"ERROR! tokenize(): Parameter sentences has type {type(sentence)} but expected {type(str)}")

    if sentence == "":
        print(f"INFO! tokenize(): Parameter sentences is empty. Will return empty list.")
        return []

    # Only import word_tokenize if we actually need to tokenise things
    from nltk import word_tokenize

    return word_tokenize(sentence)

# Provides stop word filtering
def remove_stop_words(tokens: List[str]) -> List[str]:
    """
    Removes stop words from a list of tokens.

    Input:
        tokens: List of tokens
    Output:
        result: List of filtered tokens
    """
    # Create filtering set for removing stop words
    filter_set = set()

    # Read stopwords from file
    with open('/stopwords.txt', 'r') as f:
        for word in f.readlines():
            filter_set.add(word.rstrip())

    # Return filtered sentences
    return [token for token in tokens if not token in filter_set]

# Provides stemming
def stem(tokens: List[str]) -> List[str]:
    """
    Reduce tokens to their root form.

    Input:
        tokens: List of tokens.
    Output:
        result: List of root form of tokens.
    """
    from nltk.stem import PorterStemmer

    # Create a PorterStemmer
    stemmer = PorterStemmer()

    return [stemmer.stem(token) for token in tokens]
