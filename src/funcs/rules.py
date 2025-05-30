"""
INI-powered rules for getting strings.
"""

import os
import re
from abc import ABC, abstractmethod
from urllib.parse import urlparse

class ATranslateRule(ABC):
    """
    RULES OF TRANSLATIONS!!?
    """

    """ Translation file extensions without the leading dot. """
    translateFileExt: list[str]

    names       : list[str] = []
    translations: list[str] = []
    comments    : list[str] = []

    @abstractmethod
    def TranslationGetter(this, obj: object): ...

class AInputRule(ABC):
    """
    Abstract base class for input file rules.
    """

    """ Source file extensions without the leading dot. """
    fileExt         : list[str]

    """ How to identify strings with regex """
    stringPattern   : list[str] = [
        r'(")(.+?)(")',
        r"(')(.+?)(')"
    ]

    """ 
    Input strings found in the input file.
    @see InputStringGetter will put content into this variable.
    """
    inputs          : list[str] = []

    def InputStringGetter(this, obj: str):
        """
        "Parse" the input to find all localizable strings.
        The default implementation uses regular expressions with
        @see stringPattern. Works for most languages.
        """

        for pattern in this.stringPattern:
            matches = re.findall(pattern, obj)
            for match in matches:
                # Avoid duplicates and numbers and empty strings
                if match[1].isdigit() or match[1].isdecimal() or \
                   match[1] in this.inputs or match[1].isspace() or \
                   this.isAnURL(match[1]):
                    continue
                this.inputs.append(match[1])
    
    def isAnURL(this, text: str) -> bool:
        try:
            result = urlparse(text)
            return all([result.scheme, result.netloc])
        except:
            return False

    def __init__(this, input: str, isInputAFile: bool = True):

        if isInputAFile:
            assert os.path.isfile(input)
            # t = os.path.splitext(input)
            assert os.path.splitext(input)[1].removeprefix('.') in this.fileExt

        # Leave the rest to its births

class ARule(AInputRule, ATranslateRule):
    """
    ABC does not only stand for Abstract Base Class,
    it also stands for other project types support.
    """
    ...