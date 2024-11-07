# -*- encoding: utf-8 -*-

"""
Module Involved to Normalization of Text

The normalization of text involves cleaning of text/strings from
unwanted characters like double spacing, double line breaks to single
line breaks, etc. A single functional approach is designed to handle
all such user's requests.
"""

import os
import re

def strip_whitespace(text : str, **kwargs) -> str:
    """
    Normalize Whitespaces in a Text Data

    Cleaning texts of white spaces like from beginning, end, and
    also multiple white spaces does not add any value to a text and
    should thus be removed to normalize the text.

    :type  text: str
    :param text: Original string which needs to be cleaned of
        white spaces.

    Keyword Arguments
    -----------------

    The function now provides the following additional keyword
    arguments for control:

        * **lstrip** (*bool*): Left strip white space from the
            provided text. Defaults to True. Setting any of the value
            to ``False`` overrides the default ``.strip()` function.
        * **rstrip** (*bool*): Right strip white space from the
            provided text. Defaults to True. Setting any of the value
            to ``False`` overrides the default ``.strip()` function.
        * **multiple_whitespace** (*bool*): Delete multiple spaces
            from the text. This uses the pattern cleaning using
            regular expression. Defaults to True.

    Example(s) & Use Case(s)
    ------------------------

    The function can be used to return a clean string of white spaces
    as per user requirement:

    .. code-block:: python

        statement = "  this is an example  string with  white space "

        # example of default behavior - remove all abnormal spaces::
        print(f"`{nlpurify.strip_whitespace(statement)}`")
        >>> `this is an example string with white space`

        # example of using either lstrip/rstrip/none as keywords
        print(f"`{nlpurify.strip_whitespace(statement, lstrip = False)}`")
        >>> ` this is an example string with white space`

        # example of setting multiple_whitespace
        print(f"`{nlpurify.strip_whitespace(statement, multiple_whitespace = False)}`")
        >>> `this is an example  string with  white space`

    :rtype:  str
    :return: Return a cleaner version of string free of white
        characters as per user requirement.
    """

    lstrip = kwargs.get("lstrip", True)
    rstrip = kwargs.get("rstrip", True)
    multiple_whitespace = kwargs.get("multiple_whitespace", True)

    if all([lstrip, rstrip]):
        # when both the condition is true, then default to `.strip()`
        text = text.strip()
    else:
        # we cannot use the default strip function and should be
        # handled seperately using each conditional statement
        text = text.lstrip() if lstrip else text.rstrip() if rstrip else text

    # clean the text of multiple white spaces using regular expression
    pattern = re.compile(r"\s+") # one or more white space character
    text = pattern.sub(" ", text) if multiple_whitespace else text

    return text


def normalize(text : str, strip : bool = True, **kwargs) -> str:
    """
    Normalize a Text for AI/ML Operations to Reduce Randomness

    The normalization function uses the in-built string function like
    :attr:`.strip()`, :attr:`.replace()` etc. to return a cleaner
    version. The following arguments are available for more control.
    A normalized texts may have the following properties:

        * It may not start or end with a white space character,
        * It may not have double space instead of single space, and
        * It may not be spread across multiple lines (i.e., paragraphs).

    All the above properties are desired, and can improve performance
    when used to train a large language model. Normalizaton of texts
    may also involve uniform case, typically :attr:`.lower()` that
    can be used to create a word vector.

    :type  text: str
    :param text: The base uncleaned text, all the operations are
        done on this text to return a cleaner version. The string can
        be single line, multi-line (example from "text area") and can
        have any type of escape characters.

    :type  strip: bool
    :param strip: The global attribute to clean and normalize text
        of white spaces and multiple line breaks.

    Keyword Arguments
    -----------------

    All the arguments of :func:`nlpurify.normalize.strip_whitespace()`
    is accepted. In addition, the following are specific to this
    function:

        * **strip_line_breaks** (*bool*): Strip line breaks and
            returns a single line statement. This uses the os default
            which is either "CR LF" for windows or "LF" for *nix
            based systems. However, the default value can be override
            using keyword argument :attr:`line_break_seperator`.
            Defaults to True.

        * **line_break_seperator** (*str*): The end line character
          which is either "\\r\\n" for windows or "\\n" for *nix
          based systems. By default defaults to running operating
          systems default.

        * **strip_tab_space** (*bool*): Strip a line of tab character,
            defaults to True.

    Example(s) & Use Case(s)
    ------------------------

    The function returns all scentence to default lower case, and
    strips the text filed of white spaces and multiple lines into one
    single scentence.

    .. code-block:: python

        statement = '''
        thIs Is an example  string with  \t\nwhite space

        loreememm ipsum dolor

        '''

        # default behavior removes all into single statement
        print(f"`{nlpurify.normalize(statement)}`")
        >>> `this is an example string with white space loreememm ipsum dolor`

    :rtype:  str
    :return: Return a cleaner version of string free of white
        characters as per user requirement.
    """

    line_break_seperator = kwargs.get("line_break_seperator", os.linesep)

    # normalize text of line breaks based on os/user defined
    text = text.replace(line_break_seperator, " ") \
        if kwargs.get("strip_line_breaks", True) else text
    text = text.replace(line_break_seperator, " ") \
        if kwargs.get("strip_tab_space", True) else text

    # ! 💣 always return the text in lowercase instead of user choice
    # in addition, run the white space removal logic to normalize the text
    return strip_whitespace(text, **kwargs).lower() if strip else text.lower()
