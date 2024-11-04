import re


def capitalize_sentences(text: str) -> str:
    """
    Returns the input text with the first letter of each sentence capitalized.
    Sentences are identified by the punctuation marks ., !, and ?.

    Parameters:
        text (str): The input text to be capitalized

    Returns:
        str: The text with first letter of each sentence capitalized
    """
    if not text:
        return text

    # Split into sentences while preserving delimiters
    # Check end of string OR (punctuation + optional whitespace)
    pattern = r'([.!?]|\Z)'
    sentences = re.split(pattern, text)

    # Remove empty strings and process sentences
    sentences = [s for s in sentences if s]
    result = []

    for i, part in enumerate(sentences):
        if part in '.!?':
            # If it's punctuation, add it as-is
            result.append(part)
        else:
            # If it's a sentence, capitalize first letter
            # First find the first letter in the sentence
            match = re.search(r'[a-zA-Z]', part)
            if match:
                index = match.start()
                # Convert sentence to lowercase and capitalize first letter
                processed = part[:index] + \
                    part[index].upper() + part[index + 1:].lower()
                result.append(processed)
            else:
                # No letters in this part
                result.append(part)

    return ''.join(result)
