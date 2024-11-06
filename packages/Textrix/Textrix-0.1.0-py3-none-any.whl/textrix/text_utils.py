# textrix/text_utils.py

import re
from collections import Counter

def count_words(text):
    """Counts the number of words in a given text."""
    words = re.findall(r'\b\w+\b', text.lower())
    return len(words)

def unique_words(text):
    """Returns a set of unique words in the text."""
    words = re.findall(r'\b\w+\b', text.lower())
    return set(words)

def word_frequencies(text):
    """Returns a dictionary of word frequencies in the text."""
    words = re.findall(r'\b\w+\b', text.lower())
    return dict(Counter(words))
 
