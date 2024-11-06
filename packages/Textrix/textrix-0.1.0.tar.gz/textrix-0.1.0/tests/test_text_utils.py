# tests/test_text_utils.py
from textrix.text_utils import count_words, unique_words, word_frequencies

def test_count_words():
    text = "Hello world! Hello again."
    assert count_words(text) == 4

def test_unique_words():
    text = "Hello world! Hello again."
    assert unique_words(text) == {"hello", "world", "again"}

def test_word_frequencies():
    text = "Hello world! Hello again."
    assert word_frequencies(text) == {"hello": 2, "world": 1, "again": 1}
 
