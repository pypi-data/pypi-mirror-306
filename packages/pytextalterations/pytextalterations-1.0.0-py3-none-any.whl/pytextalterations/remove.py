import re


def removepunctuation(str) -> str:
    """
    This function takes an input String and then converts it to lower case
    and removes all punctuation

    We imported regular expression to make this process easier

    Parameters: input string
    Returns: the input string without punctuation and converted to lowercase
    """
    str = re.sub(r'[^\w\s]', '', str)
    str = str.lower()
    return str