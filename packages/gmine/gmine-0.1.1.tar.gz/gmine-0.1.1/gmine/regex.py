"""Tools to evaluate user boolean input

Mission statement
-----------------
We want take a CNF string, for example, "fox or duck and chicken", to check if another string,
"The quick fox jumps over the lazy dog" satisfy the CNF.

Synopsis
------------
contains:
    Check if a my_word is contained in target.
    We use re module to check if a certain word is in a string.
satisfy:
    Evaluate if paragraph satisfies conditions.
    We split the CNF string as an array and replace the element in the array to True if words in paragraph else False.
    Except we kept "and", "or", "(" and ")" unchanged. We then rejoin the array as a string and eval the string.

"""

import re


def contains(paragraph:str, word:str) -> bool:
    """Check if a my_word is contained in target."""
    word = word.strip()
    if re.search(r'\b' + word + r'\b', paragraph):
        return True
    return False


def satisfy(paragraph: str, cnf: str)->bool:
    """Evaluate if paragraph satisfies conditions

    Examples
    --------
    >>> paragraph = "The quick fox jumps over the lazy dog"
    >>> condition1 = "fox or duck and chicken"
    >>> satisfy(paragraph, condition1)
    True

    >>> con2 = "( fox or duck ) and chicken"
    >>> satisfy(paragraph, con2)
    False

    Warnings
    --------
    Note that "and" have a higher precedence than "or". See the above example
    Also, there must be a space between paranthesis and words
    """

    cnf = cnf.split()
    for i in range(len(cnf)):
        is_word = not (cnf[i] in ["and", "or", "not", ")", "("])
        if is_word:
            if contains(paragraph, cnf[i]):
                cnf[i] = "True"
            else:
                cnf[i] = "False"

    con = ' '.join(cnf)
    return eval(con)

