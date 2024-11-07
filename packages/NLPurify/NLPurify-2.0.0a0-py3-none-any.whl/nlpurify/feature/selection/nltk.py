# -*- encoding: utf-8 -*-

"""
A Collection of Methods from the Natural Language Toolkit (NLTK)

NLTK is a leading suite of library designed for symbolic and
statistical natural language program in Python. This module is
designed for the English language, however, the due to continued
effort from the community other languages are being incorporated.

A set of functions are designed using the NLTK library for feature
selection methods like stop words removal, word lemmatizations etc.
A feature selection method works best when a text is normalized.
This can be achived by using :mod:`nlpurify.normalizeText()` method
and is generally internally by all the related functions defined.
"""

import re

from typing import Union

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nlpurify.normalization import normalize

def tokenize_text(text : str, regexp : bool = False, vanilla : bool = False, **kwargs) -> list:
    """
    Tokenization of Text into Lists of Substrings

    A word vector is one where a scentence is broken down into small
    pieces (or vectors) which constitutes the features of an model.
    To achieve tokenization, the most simpler approach is by using the
    in-built string method ``text.split()`` which splits the string
    by white characters. However, this is often in efficient and
    results in an improper model development. This can be resolved by
    using the :mod:`nltk.tokenize` methods.

    By default, the function is tuned with the ``word_tokenize``
    method which works as below:

    .. code-block:: python

        from nltk.tokenize import word_tokenize
        s = '''Good muffins cost $3.88\\nin New York.  Please buy me
            two of them.\\n\\nThanks.'''

        word_tokenize(s)
        >> ['Good', 'muffins', 'cost', '$', '3.88', 'in', 'New',
        'York', '.', 'Please', 'buy', 'me', 'two', 'of', 'them',
        '.', 'Thanks', '.']

    The power of tokenization is appreciated even more when the text
    data is cleaned and normalized as defined in the function
    :func:`nlpurify.feature.selection.nltk.remove_stopwords`.

    :type  text: str
    :param text: The raw text which is internally normalized using
        :func:`nlpurify.normalizeText()` for feature selection. To
        stop normalization of text see the keyword arguments section.

    :type  vanilla: bool
    :param vanilla: Override the :func:`nltk.tokenize.word_tokenize`
        function with Python vanilla method. Either the method allows
        setting ``regexp == True`` or ``vanilla == True`` while both
        are not allowed. The vanilla method uses string attributes
        like ``.split()`` and other keyword arguments to control
        and tokenize the data.

    :type  regexp: bool
    :param regexp: Override the :func:`nltk.tokenize.word_tokenize`
        function with a regular expressions. Either the method allows
        setting ``regexp == True`` or ``vanilla == True`` while both
        are not allowed.

    **Keyword Arguments**

    The default keyword arguments are defined for the
    :func:`nltk.tokenize.word_tokenize` function.

        * **preserve_line** (*bool*): A flag to decide whether to
          sentence tokenize the text or not, as accepted by
          the function. Defaults to False.

        * **tokenize_language** (*str*): The language model name as
          accepted by the Punkt corpus by NLTK. Defaults to the
          "english" language, as in function.

    The paramter value associated with regular expression data
    control is as below:

        * **expression** (*str*): The regular expression which
          is used to compile the regular expression. This should
          be a r-string which can be directly used. Defaults to
          ``r"\w+"` value, i.e. only word characters.

    The paramter value associated with the Python vanilla method
    control is as below:

        * **split_by** (*str*): The value is passed to :func:`split()`
          to control seperated terms, defaults to white space.

        * **retalpha** (*bool*): If set to True (default) returns only
          alphabets which is an inherent string property: ``isalpha``
          method. If both ``retalpha`` and ``retalnum`` is true, then
          ``retalpha`` has an overriding effect.

        * **retalnum** (*bool*): If set to True (default) returns only
          alphabets and numeric characters from the string which uses
          an inherent string property: ``isalnum`` method.

    **Function Example**

    The function primarily returns a list of strings which can be
    used to create word vector.

    .. code-block:: python

        s = "this is an example string, with p()nct & n0s."

        # using the default word_tokenize:
        print(nlpurify.feature_selection.tokenize_text(s))
        >> ['this', 'is', 'an', 'example', 'string', ',', 'with', 'p', '(', ')', 'nct', '&', 'n0s', '.']

        # using regular expressions, default configuration
        print(nlpurify.feature_selection.tokenize_text(s, regexp = True))
        >> ['this', 'is', 'an', 'example', 'string', 'with', 'p', 'nct', 'n0s']

        # a custom regular expressions is also accepted, feel free to experiment!
        # the following expression mimics the above example r"\w+" but using custom expression
        print(nlpurify.feature_selection.tokenize_text(s, regexp = True, expression = r"[a-zA-Z0-9_]+"))
        >> ['this', 'is', 'an', 'example', 'string', 'with', 'p', 'nct', 'n0s']

        # this is using vanilla python string functions with default values
        print(nlpurify.feature_selection.tokenize_text(s, vanilla = True))
        >> ['this', 'is', 'an', 'example', 'with']

        # to understand the difference using retalpha == False, i.e., retalnum = True
        s = "this is an example string, with p()nct & n0s. 987"
        print(nlpurify.feature_selection.tokenize_text(s, vanilla = True, retalpha = False))
        >> ['this', 'is', 'an', 'example', 'with', '987']

    **Error Guidelines**

    :raises ValueError: The error is raised when both the attribute
        ``vanilla`` and ``regexp`` is set to True.

    :raises ImportError: Error is raised when one or more nltk corpus
        is not available in the system.

    **Return Type**

    :rtype:  list[str]
    :return: Returns a tokenized list of strings. To represent and
        save the same in a tabular format use ``"".join()`` method.
    """

    preserve_line = kwargs.get("preserve_line", False)
    tokenize_language = kwargs.get("tokenize_language", "english")

    expression = re.compile(kwargs.get("expression", r"\w+"))

    split_by = kwargs.get("split_by", " ")
    retalpha = kwargs.get("retalpha", True)
    retalnum = kwargs.get("retalnum", True)

    tokenize_method = None
    # ! do not allow both `regexp` and `vanilla` as true
    if all([regexp, vanilla]):
        raise ValueError("Both Control are Not Allowed.")
    elif any([regexp, vanilla]):
        # ? if the error is not raised, execute below - else section
        if regexp:
            tokenize_method = "regexp"
        else:
            # ? vanilla method is selected, however based
            # on keyword selection - setting different index
            if retalpha:
                # this has an ovverriding effect thus first
                tokenize_method = "vanilla-alnum"
            elif retalnum:
                tokenize_method = "vanilla-alpha"
            else:
                tokenize_method = "vanilla-vanilla"
    else:
        tokenize_method = "word-tokenize"

    # select method and parameter control, and finally
    # return token data value from the choice of method:
    tokens = {
        "regexp" : expression.findall(text),

        # we've the three methods of vanilla like:
        "vanilla-alnum" : [s for s in text.split(split_by) if s.isalnum()],
        "vanilla-alpha" : [s for s in text.split(split_by) if s.isalpha()],
        "vanilla-vanilla" : text.split(split_by), # default, no change

        "word-tokenize" : word_tokenize(text, language = tokenize_language, preserve_line = preserve_line)
    }

    return tokens[tokenize_method]


def remove_stopwords(text : str, language : str = "english", rtype : object = str, **kwargs) -> Union[str, list]:
    """
    Function to Remove Stopwods from a Raw Text using NLTK

    In a Natural Language Processing (NLP), stopwords are frequently
    removed to improve the performance of the model and increase the
    computational efficiency. Words like "and", "or", etc. does not
    provide additional information to the model but are important for
    communications.

    The NLTK library hosts a lists of words that should be removed.
    To find the list of supported language, check the fields:

    .. code-block:: python

        from nltk.corpus import stopwords
        print(stopwords.fileids()) # list of supported language

    Stopwords is available under :mod:`nltk.corpus` which is required
    by the function. To download a corpus:

    .. code-block:: python

        import nltk
        nltk.download("all") # download all the available corpus
        nltk.download("stopwords") # only download stopwrds corpus

    While it is advisable to download all the corpus, but it is
    left on the discretion of the user. The function may throw an
    error in case there are additional dependent corpus which needs
    to be downloaded.

    :type  text: str
    :param text: The raw text which is internally normalized using
        :func:`nlpurify.normalizeText()` for feature selection. To
        stop normalization of text see the keyword arguments section.

    :type  language: str
    :param language: The name of the language which is available
        under the :mod:`nltk.corpus.stopwords`. To find the list
        of accepted languages check ``stopwords.fields()``. Defaults
        to the "english" language.

    **Keyword Arguments**

        * **tokenize** (*bool*): Tokenize the text using the
          :mod:`nltk.tokenize.word_tokenize()` method to extract the
          tokens from the strings which returns the syllables from
          a single word. Defaults to True. If false, the function
          internally creates a token vector using ``text.split()``
          method, which splits the words by spaces - which may
          have unwanted effect when symbols are present in the text.
          Check attributes of :func:`tokenize()` for more details.

        * **normalize** (*bool*): Normalize the text internally.
          Defaults to true, else if the data is already normalized
          then pass False. Note the function may not be able to
          remove all the stopwords if the data is not normalized and
          the case of the words is not lower.

    **Function Example**

    For more control over the tokenization, all the parameters
    of :func:`tokenize_text()` is accepted.

    .. code-block:: python

        s = "this is an example string, with p()nct & n0s."

        # using defaults from tokenize_text, i.e., using word_tokenize
        print(nlpurify.feature_selection.remove_stopwords(s))
        >> example string , p ( ) nct & n0s .

        # this we can further simplify by using other features
        print(nlpurify.feature_selection.remove_stopwords(s, regexp = True))
        >> example string p nct n0s

    **Error Guidelines**

    :raises ValueError: The error is raised when the return type is
        not in {str, list} values. Make sure the data type is an type
        instance and is not passed as a string value.

    :raises ImportError: Error is raised when one or more nltk corpus
        is not available in the system.

    **Return Type**

    :rtype:  str | list
    :return: A cleaned string or a vector (*iterable*) of selected
        features from a given text message.
    """

    tokenize = kwargs.get("tokenize", True)
    normalize = kwargs.get("normalize", True)

    stopwords_ = stopwords.words(language) # defaults to english

    # ? normalize the text using nlpurify.normalizeText()
    # else, left at user's discreations or additional functionalities
    text = normalize(
        text,
        uniform_text_case = "lower",
        strip_line_breaks = True
    ) if normalize else text

    tokens = tokenize_text(text, **kwargs) if tokenize else text
    tokens = [word for word in tokens if word not in stopwords_]

    # ensure return type of the data, else raise error
    if rtype not in [str, list]:
        raise ValueError(f"Accepted arguments ``list`` or ``str`` received {rtype}.")

    return " ".join(tokens) if rtype == str else tokens
