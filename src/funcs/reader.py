import os
import re
from pathlib import Path
from typing import Generator
from . import types
from .. import globs

def ReadResFile(path: str) -> types.ATranslationFile:
    result = types.ATranslationFile()
    result.read(path)
    return result

def ReadXAMLFile(path: str) -> list[str]:
    """
    Gets all strings inside the specified XAML path.
    """

    results: list[str] = []

    with open(path, "r") as f:
        content = f.read()
        matches = re.findall(
            r'([.\S]+?)([\s]*)=([\s]*)(")([.\s]+?)(")',
            #  ^^^^^^^ Attribute/DependencyProperty set
            #          ^^^^^^^ Tabs/spaces/newlines
            #                 ^ The equal sign ofc
            #                  ^^^^^^^^^^^ Tabs/spaces/newlines
            #                         ^^^^^^^^^^^^^^^ Content  
            content
        )

        for match in matches:
            # Simplify the match
            attrib: str = match[0].strip()
            attribcontent: str = match[4]

            # Avoid duplicates
            #       numbers
            #       empty strings
            #       Binding`s, *Resource, x:Class etc
            #       xml namespaces
            if attrib.startswith("xmlns:") or attrib.startswith("x:") \
               or not attribcontent or attribcontent.startswith("{x:") \
               or attribcontent.startswith("{Binding ") \
               or attribcontent.startswith("{StaticResource ") \
               or attribcontent.startswith("{ThemeResource ") \
               or attribcontent.isdigit() or attribcontent.isdecimal() \
               or attribcontent.isspace() or attribcontent in results: continue
            
            results.append(attribcontent)

    return results

def ReadSourceFile(path: str) -> list[str]:
    """
    Gets all strings inside the specified
    source code path.

    Almost the same with [`ReadXAMLFile`],
    with regex pattern and check modifications.
    """

    results: list[str] = []

    with open(path, "r") as f:
        content = f.read()
        matches = re.findall(
            r'(["\'])([.\s]+?)(["\'])', 
            content
        )

        for match in matches:
            # Simplify the match
            string = match[1]

            # Avoid duplicates
            #       numbers
            #       empty strings
            if not string or string in results \
               or string.isdigit() or string.isdecimal() \
               or string.isspace(): continue
            
            results.append(string)

    return results

def GetLanguagesList() -> Generator[str]:
    for path in Path(globs.settings.output_dir).iterdir():
        if path.is_dir() and \
           [f for f in path.iterdir()
              if f.is_file() and os.path.splitext(f)[0] in globs.settings.filename]:
            yield path.name
