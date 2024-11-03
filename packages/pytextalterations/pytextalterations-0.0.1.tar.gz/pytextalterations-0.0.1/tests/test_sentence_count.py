import pytest
from pytextalterations.sentence_count import sentence_count

text_1 = "Hello world! How are you? I am fine."
text_with_abbrv = "Dr. Smith went to the hospital. He arrived at 5 p.m."
text_with_abbrv_2 = "The U.S. is a country. Across the ocean from the U.S. is the U.K."
text_with_consecutive_punctuation = "Seriously?! There's no way!"
text_with_ellipsis = "Well... I'm not sure. But it seems okay."

def test_1():
    assert sentence_count(text_1) == 3

def test_with_abbrv():
    assert sentence_count(text_with_abbrv) == 2

def test_with_abbrv_2():
    assert sentence_count(text_with_abbrv_2) == 2

def test_with_consecutive_punctuation():
    assert sentence_count(text_with_consecutive_punctuation) == 2

def test_with_ellipsis():
    assert sentence_count(text_with_ellipsis) == 2

def test_no_text():
    assert sentence_count("") == 0

def test_no_punctuation():
    assert sentence_count("This is a single line without punctuation") == 1

def test_single_abbrv():
    assert sentence_count("Prof. Smith") == 1
