import pytest
from pytextalterations.capitalize_sentences import capitalize_sentences


def test_capitalize_sentences():
    # Test basic sentence capitalization
    assert capitalize_sentences(
        "hello world. how are you?") == "Hello world. How are you?"

    # Test empty string
    assert capitalize_sentences("") == ""

    # Test lowercase sentence
    assert capitalize_sentences("hello world") == "Hello world"

    # Test sentences with different punctuation
    assert capitalize_sentences(
        "hello! how are you. fine thanks?") == "Hello! How are you. Fine thanks?"

    # Test sentences with every word capitalized
    assert capitalize_sentences(
        "Hello World. How Are You?") == "Hello world. How are you?"

    # Test alternating letters of capitalized/lowercase
    assert capitalize_sentences(
        "mIxEd cAsE. wOrDs hErE!") == "Mixed case. Words here!"

    # Test punctuation
    assert capitalize_sentences(
        "h.e.l.l.o! world") == "H.E.L.L.O! World"
