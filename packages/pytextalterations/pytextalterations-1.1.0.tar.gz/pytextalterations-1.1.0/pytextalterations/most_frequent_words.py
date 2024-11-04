def most_frequent_words(text: str, num_words: int = 0) -> list[str]:
    """
    Returns the num_words most frequent words in the text as a list.
    The list will be sorted from most frequent to least frequent.
    If num_words = 0, all words will be returned.

    Words are separated by spaces.

    Parameters:
    text (str): The input text
    num_words (int): The number of words to be returned

    Returns:
    list[str]: the most frequent words, sorted by frequency
    """ 
    if (num_words < 0):
        raise ValueError("Number of words should not be negative")

    words = text.split(' ')

    counter = {}
    
    for word in words:
        if word not in counter:
            counter[word] = 0
        counter[word] += 1

    unique_words = list(counter.keys())

    if (num_words == 0):
        num_words = len(unique_words)

    unique_words.sort(key=lambda word: counter[word], reverse=True)

    return unique_words[:num_words]
    
