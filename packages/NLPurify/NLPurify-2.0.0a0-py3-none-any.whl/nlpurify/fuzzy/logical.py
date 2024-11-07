# -*- encoding: utf-8 -*-

"""
Creates an Extension to Perform Logical Operations

Logical operations like ``and`` or ``or`` can be implemented with the
module. This reduces manual intervention like using repeated for-loop
and/or conditional statements for the end user.
"""

from typing import List
from nlpurify.fuzzy.wrapper import fuzzy_score

class LogicalFuzzy:
    """
    The Logical Fuzzy is an Extension of Scoring for Logical Operation

    The logical operations can be integrated to search more than one
    reference string from a statement. This allows more control and
    also reduces repeated function call involving loops and other
    conditional statements.

    :type  string: str
    :param string: The original string against which the reference
        values are to be checked and validated.

    :type  references: list
    :param references: A list of n-references against which fuzzy
        score is determined. The score is also a n-length array.

    :type  method: str
    :param method: Amy of the supported method :func:`fuzzywuzzy.fuzz`
        module, defaults to "partial_ratio" method.

    .. code-block:: python

        statement = "a quick brown fox jumps over a lazy dog"

        # let's create an object to calculate and score the statement
        logical_fuzzy = nlpurify.fuzzy.LogicalFuzzy(statement, "quick", "foxy")

        # let's check the individual score of `quick` and `foxy` against statement
        print(logical_fuzzy.fuzzy_scores())
        >> [100, 75]

        # now we can have both the logical and controls like:
        print(logical_fuzzy.evaluate(80, logic = "any", operator = "<="))
        >> True # 100 <= 80 and 75 <= 80

        print(logical_fuzzy.evaluate(80, logic = "all"))
        >> False # 100 >= 80 and 75 >= 80
    """

    def __init__(
        self,
        string : str,
        *references : List[str],
        method : str = "partial_ratio"
    ) -> None:
        self.string = string

        # list of any n-reference strings for fuzzy scoring
        self.references = references

        # mandatory keyword arguments which determines the fuzzy
        # the method is any of the supported argument of the fuzzy
        self.method = method


    def fuzzy_scores(self) -> list:
        """
        Calculate Fuzzy Score of Each Reference to Statement

        The internal function iterates for each reference string to
        score the similarity against the statement using the internal
        :func:`nlpurify.fuzzy.wrapper.fuzzy_score()` method.
        """

        return [
            fuzzy_score(self.string, reference, self.method)
            for reference in self.references
        ]


    def evaluate(self, thresh : int, logic : str, operator : str = ">="):
        """
        Evaluate the Final Score using Operators

        The operator like :attr:`>=`, :attr:`<=` is dynamic and thus
        provides additional controls to the logical operations as it
        can now be used to efficiently negate both the side of the
        curve for sequence matching. The operator is used internally
        and is evaluated using the :func:`eval()` to determine the
        final result and provide the score.

        :type  logic: str
        :param logic: The logical operator which is either :attr:`all`
            i.e., and condition and :attr:`any` which is or condition.

        :type  operator: str
        :param operator: The deterministic operator which can be used
            to efficiently control both the side of the curve for
            fuzzy scoring.
        """

        scores = self._fuzzy_score_()
        return eval(f"{logic}([score {operator} {thresh} for score in {scores}])")
