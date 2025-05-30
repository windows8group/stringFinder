"""
Support for C# GUI applications
made with Microsuck works.
"""

import os
from . import rules
from .. import globs
import xml.etree.ElementTree as ET

class MSResRule(rules.ATranslateRule):
    translateFileExt = [ "resx", "resw" ]

    def TranslationGetter(this, obj: object):
        assert isinstance(obj, ET.Element)

        for child in obj.iter("data"):
            this.names.append(str(child.attrib["name"]))

            valueElm = child.find("value")
            if valueElm is not None:
                this.translations.append(str(valueElm.text))
            else:
                this.translations.append("")

            commentElm = child.find("comment")
            if commentElm is not None:
                this.comments.append(str(commentElm.text))
            else:
                this.comments.append("")

class MicroSuck(rules.ARule):
    fileExt = [
        "cs",               # C#
        "cpp", "c",         # C++ implementations
        "hpp", "h",         # C++ headers
        "vb", "cls", "bas", # Visual Basic
        "xaml"              # XAML, XML but used to design UI
    ]

    translateFileExt = [ "resx", "resw" ]

    isXAML: bool

    def __init__(this, input: str, isInputAFile: bool = True):
        rules.ARule.__init__(this, input, isInputAFile)

        this.isXAML = isInputAFile and os.path.splitext(input)[1] == ".xaml"

        assert globs.outputPath

        this.TranslationGetter(ET.parse(globs.outputPath).getroot())

        if isInputAFile:
            with open(input, "r", encoding="utf-8") as f:
                this.InputStringGetter(f.read())
        else:
            this.InputStringGetter(input)

    def TranslationGetter(this, obj: object):
        assert isinstance(obj, ET.Element)

        for child in obj.iter("data"):
            this.names.append(str(child.attrib["name"]))

            valueElm = child.find("value")
            if valueElm is not None:
                this.translations.append(str(valueElm.text))
            else:
                this.translations.append("")

            commentElm = child.find("comment")
            if commentElm is not None:
                this.comments.append(str(commentElm.text))
            else:
                this.comments.append("")

    def InputStringGetter(this, obj: str):
        if this.isXAML:
            import re
            matches = re.findall(r'(.+?)=(")(.+?)(")', obj)
            for match in matches:
                # Simplify the match
                attrib = match[0].strip()
                content = match[2]

                # Avoid duplicates and numbers and empty strings
                # Avoid ones with xmlns: + x: prefixes too
                if content.isdigit() or content.isdecimal() or \
                   content in this.inputs or content.isspace() or \
                   attrib.startswith("xmlns:") or attrib.startswith("x:"):
                    continue
                this.inputs.append(content)
        else:
            rules.ARule.InputStringGetter(this, obj)