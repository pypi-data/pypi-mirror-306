# Python Package Exercise

An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

# Badges
![Tests Workflow Status](https://github.com/software-students-fall2024/3-python-package-subwaysurfers/actions/workflows/tests.yml/badge.svg)
![Build Workflow Status](https://github.com/software-students-fall2024/3-python-package-subwaysurfers/actions/workflows/event-logger.yml/badge.svg)

# About

Text Alterations is a package that alters text in four different ways.

With this package you can:
1. Capitalize the first letter of sentences in a text
2. List words in a text in order of frequency
3. Find the number of sentences in a text
4. Remove all the punctuation and capital letters in a text

# Link

Find our package on PyPI [here](https://pypi.org/project/pytextalterations/)

# Functions

## 1. Capitalize Sentences
### capitalize_sentences(text: str) -> str:

Returns the input text with the first letter of each sentence capitalized.
Sentences are identified by the punctuation marks ., !, and ?.

Parameters:
        text (str): The input text to be capitalized

Returns:
        str: The text with first letter of each sentence capitalized

### For example:

string = 'i am a student at NYU. i like software engineering. this class is valuable to my education.'

capitalize_sentences(string) returns:

'I am a student at NYU. I like software engineering. This class is valuable to my education.'

## 2. Most Frequent Words

### most_frequent_words(text: str, num_words: int = 0) -> list[str]:

Returns the num_words most frequent words in the text as a list.
The list will be sorted from most frequent to least frequent.
If num_words = 0, all words will be returned.
Words are separated by spaces.

Parameters:
    text (str): The input text
    num_words (int): The number of words to be returned

Returns:
    list[str]: the most frequent words, sorted by frequency

### For example:

string = 'i am a student at NYU. i like software engineering. this class is valuable to my education.'

most_frequent_words(string) returns:

['i', 'am', 'a', 'student', 'at', 'NYU.', 'like', 'software', 'engineering.', 'this', 'class', 'is', 'valuable', 'to', 'my', 'education.']

## 3. Remove Punctuation

### removepunctuation(str) -> str:
This function takes an input String and then converts it to lower case
and removes all punctuation

We used regular expression to make this process easier

Parameters: 
    text(str): input string
Returns: 
    str: the input string without punctuation and converted to lowercase

### For example:

string = 'i am a student at NYU. i like software engineering. this class is valuable to my education.'

removepunctuation(string) returns:

'i am a student at nyu i like software engineering this class is valuable to my education'

## 4. Sentence Count

### sentence_count(text: str) -> int:
Returns the number of sentences in the text string.
This function identifies sentences and accounts for
several common abbreviations but not all abbreviations.
    
Parameters:
    text (str): The input text
    
Returns:
    int: The number of sentences in the input text.

### For example:

string = 'i am a student at NYU. i like software engineering. this class is valuable to my education.'

sentence_count(string) returns:

3

# Contribute

### Please install a virtual environment of your choice
#### In this example, we will use pipenv

pip install pipenv

### Please clone the repo 
git clone https://github.com/software-students-fall2024/3-python-package-subwaysurfers.git

cd 3-python-package-subwaysurfers

### Install dev packages and activate the virtual environment

pipenv install --dev

pipenv shell

### Build
pip install build

python -m build

### Run unit tests
pytest 

# Installation and Usage

### Create and activate a virtual environment of your choice
#### In this example, we will use pipenv
pip install pipenv

pipenv shell

### Install our package! 
pipenv install pytextalterations

## To run
### Run our package 
python -m pytextalterations

You will see a screen that looks like this:

***
Welcome to Text Alterations

With this package you can:

(C) Capitalize the first letter of sentences in a text

(F) List words in a text in order of frequency

(N) Find the number of sentences in a text

(R) Remove all the punctuation and capital letters in a text

Please choose an option (C, F, N, R, or Quit) to continue:

***

Enjoy!

# Group Members
Neha Magesh: [link](https://github.com/nehamagesh)
Luca Ignatescu: [link](https://github.com/LucaIgnatescu)
James Whitten: [link](https://github.com/jwhit0)
Tahsin Tawhid: [link](https://github.com/tahsintawhid)