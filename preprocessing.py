"""
Module for preprocessing a list of sentences.
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


#### OLD CODE: Works on lists, as opposed to single string. Daniel did goof.

# # Provides tokenisation
# def _tokenize(sentences: List[str]) -> List[List[str]]:
#     """
#     Parses and tokenizes a set of sentences and returns a list of lists of tokens, per sentence.

#     Input:
#         sentences: List of sentences in form 'str' per sentence.
#     Output:
#         result: List of tokenised sentences in form 'List[str]' per sentence
#     """
#     # Check if we have a list
#     if not isinstance(sentences, list):
#         exit(f"ERROR! tokenize(): Parameter sentences has type {type(sentences)} but expected {type(list)}")
    
#     if sentences == []:
#         print(f"INFO! tokenize(): Parameter sentences is empty. Will return empty list.")
#         return []
    
#     # Only import word_tokenize if we actually need to tokenise things
#     from nltk import download
#     from nltk import word_tokenize

#     # Download the resources for tokenisation (tokenizers/punkt/PY3/english.pickle)
#     download('punkt')

#     # Create result list
#     result = []

#     # For each sentence
#     for sentence in sentences:
#         # Create a tokens list using nltk
#         sentence_tokens = word_tokenize(sentence)

#         # Add tokens for this sentence to the results list.
#         result.append(sentence_tokens)

#     # Extra check for flattened list.
#     if [token for sentence_list in result for token in sentence_list] == []:
#         print(f"INFO! tokenize(): Somehow, results contains only empty lists.")

#     return result

# # Provides stop word filtering
# def _remove_stop_words(tokenised_sentences: List[List[str]]) -> List[List[str]]:
#     """
#     Removes stop words from a list of tokenised sentences, and returns the results.

#     Input:
#         tokenised_sentences: List of tokenised sentences in form 'List[str]' per sentence
#     Output:
#         result: List of tokenised sentences without stop words, in form 'List[str]' per sentence
#     """
#     # Create filtering set for removing stop words
#     filter_set = set()
    
#     # Read stopwords from file
#     with open('/stopwords.txt', 'r') as f:
#         for word in f.readlines:
#             filter_set.add(word.rstrip())

#     # Create result list
#     result = []

#     # Perform stop word removal for each tokenised sentence
#     for tokenised_sentence in tokenised_sentences:
#         # Only add tokens that are not present in the filter set.
#         filtered_sentence = [token for token in tokenised_sentence if not token in filter_set]
        
#         # Add filtered sentence to result
#         result.append(filtered_sentence)

#     # Return filtered sentences
#     return result

# # Provides stemming
# def _stem(tokenised_and_filtered_sentences: List[List[str]]) -> List[List[str]]:
#     """
#     Reduce tokens to their root form.

#     Input:
#         tokenised_and_filtered_sentences: List of tokenised sentences without stop words in form 'List[str]' per sentence
#     Output:
#         result: List of root forms of tokenised sentences without stop words, in form 'List[str]' per sentence
#     """
#     from nltk.stem import PorterStemmer

#     # Create a PorterStemmer
#     stemmer = PorterStemmer()

#     # Create result list
#     result = []

#     # Perform stemming for each filtered tokenised sentence
#     for sentence in tokenised_and_filtered_sentences:
#         # Only add tokens that are not present in the filter set.
#         stemmed_sentence = [stemmer.stem(token) for token in sentence]
        
#         # Add filtered sentence to result
#         result.append(stemmed_sentence)

#     # Return stemmed sentences
#     return result
