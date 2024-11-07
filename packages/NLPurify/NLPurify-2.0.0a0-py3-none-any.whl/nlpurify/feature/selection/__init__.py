# -*- encoding: utf-8 -*-

"""
Feature Selection from a Raw Text Data

A feature selection is designed to improve the performance of a NLP
module by recursive eliminations. For example, stopwords does not
contribute to improve the performance of the model and is usually
removed from a text which provides a better model accuracy.
"""

from nlpurify.feature.selection.nltk import * # noqa: F401, F403 # pyright: ignore[reportMissingImports]
