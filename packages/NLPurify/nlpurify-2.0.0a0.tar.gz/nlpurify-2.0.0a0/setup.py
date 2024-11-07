#!/usr/bin/env python
#
# Copywright (C) 2024 Debmalya Pramanik <neuralNOD@gmail.com>
# LICENSE: MIT License

from setuptools import setup
from setuptools import find_packages

import nlpurify as nlpu

setup(
    name = "NLPurify",
    version = nlpu.__version__,
    author = "shark-utilities developers",
    author_email = "neuralNOD@outlook.com",
    description = "Text cleaning and feature extractions using NLP, Traditional approach.",
    long_description = open("README.md", "r").read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/sharkutilities/NLPurify",
    packages = find_packages(),
    classifiers = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License"
    ],
    project_urls = {
        "Issue Tracker" : "https://github.com/sharkutilities/NLPurify/issues",
        # "Code Documentations" : "https://.readthedocs.io/en/latest/index.html",
        "Org. Homepage" : "https://github.com/sharkutilities"
    },
    keywords = [
        # keywords for finding the package::
        "nlp", "text-cleaning", "nlp-cleaning", "llm",
        "utility", "utilities", "util", "utils", "functions",
        # keywords for finding the package relevant to usecases::
        "wrappers", "data science", "data analysis", "data scientist", "data analyst"
    ],
    python_requires = ">=3.8"
)
