# TODO @ Jens: Check if you agree with how I do this.
"""
Module for preprocessing a list of sentences.
Contains methods for tokenisation, stop-word filtering, and stemming.
"""

from typing import List

def tokenize(sentences: List[str]) -> List[List[str]]:
    """
    Parses and tokenizes a set of sentences and returns a list of lists of tokens, per sentence.

    Input:
        sentences: List of strings.
    Output:
        tokens: List of lists, one per string input, consisting of its tokens.
    """
    # Check if we have a list
    if not isinstance(sentences, list):
        print(f"tokenize(): Parameter sentences has type {type(sentences)} but expected {type([])}")
        exit(1)
    
    if sentences == []:
        print(f"tokenize(): Parameter sentences is empty. Will return empty list.")
        return []
    
    # Only import word_tokenize if we actually need to tokenise things
    from nltk import word_tokenize
        
    # Create result list
    result = []

    # For each sentence
    for sentence in sentences:
        # Create a tokens list using nltk
        sentence_tokens = word_tokenize(sentence)

        # Add tokens for this sentence to the results list.
        result.append(sentence_tokens)

    # After tokenisation, return the result list in both normal and flattened manner
    # TODO: Remove flattened results if not needed.
    flattened_results = [token for sentence_list in result for token in sentence_list]

    if flattened_results == []:
        print(f"tokenize(): Somehow, results contains only empty lists.")

    return result

def remove_stop_words(tokenised_sentences: List[List[str]]) -> List[List[str]]:
    # TODO: Implement method.
    from nltk.corpus import stopwords

    # Create filtering set for removign stop words
    filter_set = set(stopwords.words('english'))

    # Possibly add custom words
    custom_filter_set = set("")
    filter_set = filter_set.union(custom_filter_set)

    # Create result list
    result = []

    # Perform stop word removal for each tokenised sentence
    for tokenised_sentence in tokenised_sentences:
        # Only add tokens that are not present in the filter set.
        filtered_sentence = [token for token in tokenised_sentence if not token in filter_set]
        
        # Add filtered sentence to result
        result.append(filtered_sentence)

    # Return filtered sentences
    return result

def stem(tokenised_and_filtered_sentences: List[List[str]]) -> List[List[str]]:
    # TODO: Implement method
    from nltk.stem import PorterStemmer

    # Create a PorterStemmer
    stemmer = PorterStemmer()

    # Create result list
    result = []

    # Perform stemming for each filtered tokenised sentence
    for sentence in tokenised_and_filtered_sentences:
        # Only add tokens that are not present in the filter set.
        stemmed_sentence = [stemmer.stem(token) for token in sentence]
        
        # Add filtered sentence to result
        result.append(stemmed_sentence)

    # Return stemmed sentences
    return result
