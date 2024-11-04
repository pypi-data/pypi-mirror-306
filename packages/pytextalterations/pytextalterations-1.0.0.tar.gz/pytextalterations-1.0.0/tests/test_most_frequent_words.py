import pytest
from pytextalterations.most_frequent_words import most_frequent_words

text = "abc def abc def a a b b c de f g abc"

frequencies = {
    'abc': 3,
    'def': 2,
    'a': 2,
    'b': 2,
    'c': 1,
    'de': 1,
    'f': 1,
    'g': 1
}
def test_default():
    words = most_frequent_words(text)
    assert words == ['abc', 'def', 'a','b', 'c', 'de', 'f', 'g']

def test_num_words_1():
    words = most_frequent_words(text, 1)
    assert words == ['abc']

def test_num_words_2():
    words = most_frequent_words(text, 3)
    assert words == ['abc', 'def', 'a']

def test_invalid_num_words():
    with pytest.raises(ValueError):
        words = most_frequent_words(text, -1)

