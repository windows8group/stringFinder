import argparse
import os.path
import sys

from wx import App
from . import globs
from libtextworker.general import logger, logpath, test_import

def main():
    logger.info("The log file is %s", logpath)
    test_import("wx")

    parser = argparse.ArgumentParser(sys.argv[0], epilog=
"""
Finds all strings inside a code project, localize them.\n
Made specifically for Windows applications.\n
(C) 2025 Windows8Group the team.\n\n
Some settings (in/out paths, languages) are saved to ~/.stringFinder/settings.json.
""")
    parser.add_argument("paths", nargs="*", help="input files/folders/both")
    parser.add_argument("--output", "-o", nargs=1, metavar="PATH", help="output directory", type=str)
    parser.add_argument("--language", "-l", action="extend", type=str, metavar="LANGUAGE", help="languages", nargs="+")
    parser.add_argument("--silent", "-s", const=False, nargs="?", metavar="BOOLEAN", help="do not show GUI")

    options: argparse.Namespace = parser.parse_args()
    logger.info("Main file: %s", sys.argv[0])

    for path in options.paths:
        if os.path.isfile(path):
            logger.info("%s is a file", path)
            globs.settings.source_files.append(path)
        else:
            logger.info("%s is a directory", path)
            globs.settings.source_dirs.append(path)
    
    if options.output:
        logger.info("Output directory: %s", options.output)
        globs.settings.output_dir = options.output
    
    if options.language:
        globs.settings.languages = options.languages
        logger.info(f"Languages: {options.languages}")
    
    if not bool(options.silent):
        app = App(clearSigInt=True)
        app.SetAppName("stringFinder")
        app.SetAppDisplayName("stringFinder")

        from .mainwindow import MainWindow
        wind = MainWindow()
        app.SetTopWindow(wind)
        wind.Show()

        app.MainLoop()