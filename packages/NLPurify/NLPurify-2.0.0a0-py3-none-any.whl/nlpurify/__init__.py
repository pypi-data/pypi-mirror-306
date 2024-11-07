# -*- encoding: utf-8 -*-

"""
Text Cleaning and Feature Extraction Engine

The module provides text cleaning and feature extractions (like
mobile number, url, etc.) from a Python string and also provides an
one-stop solution library oriented towards text cleaning.
"""

# ? package follows https://peps.python.org/pep-0440/
# ? https://python-semver.readthedocs.io/en/latest/advanced/convert-pypi-to-semver.html
__version__ = "v2.0.0.a0"

# init-time options registrations
from nlpurify import fuzzy

from nlpurify.feature import (
    selection as feature_selection
)

from nlpurify.normalization import (
    normalize,
    strip_whitespace
)
