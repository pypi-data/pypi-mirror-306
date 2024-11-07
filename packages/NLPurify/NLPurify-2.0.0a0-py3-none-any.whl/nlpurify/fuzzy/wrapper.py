# -*- encoding: utf-8 -*-

from fuzzywuzzy import fuzz

def fuzzy_score(string : str, reference : str, method : str = "partial_ratio") -> int:
    """
    A Function to Score two Sequences `string` and `reference` with Fuzzy

    The `fuzzywuzzy.fuzz` provides a number of options to score two
    sequences of a string based on different methods like the "partial
    ratio", "token sort ratio" etc. The function acts as a wrapper to
    chosse any of the method which calls one of the internal function
    to score two sequences.

    NOTE: The function is directly taken of the :func:`nlpurify.legacy`
    code and end users are requested to move to the new method instead.

    :type  string: str
    :param string: The original string against which the scoring is
        determined of the reference string.

    :type  reference: str
    :param reference: The reference string or sequence which is scored
        based on the matching with the original string.

    :type  method: str
    :param method: The name of the method based on which the scoring is
        to be calculated. This can be any of the string as available in
        the original module. Defaults to "partial_ratio" method.
    """

    method = {
        "ratio" : fuzz.ratio,
        "partial_ratio" : fuzz.partial_ratio,
        "token_sort_ratio" : fuzz.token_sort_ratio
    }.get(method)

    return method(reference, string)
