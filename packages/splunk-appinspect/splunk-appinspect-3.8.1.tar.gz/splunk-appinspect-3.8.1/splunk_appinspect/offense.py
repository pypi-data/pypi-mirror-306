# Copyright 2019 Splunk Inc. All rights reserved.

"""
A naive profanity scanner.  It flags any words contained in banned_wordlist.txt, optionally with suffixes 'er' or 'ing'.
"""
import os
import re
from pathlib import Path

import magic

exceptions = ["heller"]
suffixes = ["", "er", "ing"]

with open(Path(os.path.abspath(__file__)).parent / "banned_wordlist.txt") as _file:
    words_array = []
    for _line in _file:
        banned_word = _line.strip().lower()
        for suffix in suffixes:
            words_array.append((banned_word + suffix, banned_word))
    words = dict(words_array)


def word_is_profane(word):
    """
    Match a single word against our wordlist

    This can probably be substantially accelerated using a precomputed set rather than iterating
    through the wordlist (and variations) each time.
    """
    lc_word = word.lower()
    if lc_word in exceptions:
        return None
    if lc_word in words:
        return word, words[lc_word]

    return None


def scan_file(filename: Path):
    """
    Tokenize into single words, and match each against our banned word list.
    Notice: This method should only be used in Unix environment.
    """
    results = set()
    if get_mime_type(filename).find("text") == -1:
        # Skip binary files
        return results
    with open(filename, "r", errors="ignore") as file:
        lineno = 0
        for line in file:
            lineno += 1
            for word in re.split(r"\W+", line):
                match = word_is_profane(word)
                if match:
                    results.add((lineno, line.strip(), match[0], match[1]))
    return results


def get_mime_type(file: Path):
    """
    Call out to the OS to determine whether this file is text or binary (we
    don't want to scan binary files).
    Notice: This method should only be used in Unix environment.
    """
    output = magic.from_file(str(file), mime=True)
    parts = output.split(";")
    return parts[0]
