"""
Tests for count_words() in word_freq.py.

count_words(path, ...) opens a FILE itself, so each test must create a real
file first. tmp_path makes that safe.
"""

import pytest
from word_freq import count_words


# tmp_path is a BUILT-IN pytest fixture (you don't define it anywhere). It
# gives each test its own empty temporary folder, deleted afterwards, so
# tests never touch your real files.
def test_count_words_reads_file(tmp_path):
    f = tmp_path / "sample.txt"                 # a path inside the temp folder
    f.write_text("apple apple banana")          # ARRANGE: create the file

    # use_stopwords=False keeps every word. With the default (True) common
    # words such as "a" would be filtered out and change the result.
    # A Counter equals a plain dict with the same contents, so this works.
    assert count_words(f, use_stopwords=False) == {"apple": 2, "banana": 1}


# The same test body runs three times with different text and settings.
@pytest.mark.parametrize("text, min_length, expected", [
    ("apple fig apple", 1, {"apple": 2, "fig": 1}),   # keep all words
    ("apple fig apple", 4, {"apple": 2}),             # "fig" is shorter than 4
    ("", 1, {}),                                      # empty file, empty result
], ids=["all-words", "min-length-filters-short", "empty-file"])
def test_min_length(tmp_path, text, min_length, expected):
    f = tmp_path / "sample.txt"
    f.write_text(text)                          # the text comes from the table row
    assert count_words(f, min_length=min_length, use_stopwords=False) == expected