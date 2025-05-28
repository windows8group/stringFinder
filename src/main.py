import argparse
import os.path
import sys

from wx import App
import globs
from libtextworker.general import logger, logpath, test_import

if __name__ == "__main__":
    logger.info("The log file is %s", logpath)
    test_import("wx")

    parser = argparse.ArgumentParser(sys.argv[0], description=
"""
Finds all strings inside a code project, localize them.\n
(C) 2025 Windows8Group the team.
""")
    parser.add_argument("paths", nargs="*", help="file(s) and/or folder(s) to be used")
    parser.add_argument("--string-char", "-c", const='"', nargs="?", metavar="CHAR",
                        help = "Character used to mark a string (defaults to double quotes)")
    parser.add_argument("--output", "-o", nargs=1, metavar="PATH", help = "Output file path")
    parser.add_argument("--silent", "-s", const=False, nargs="?", metavar="BOOOLEAN", help="Do now show GUI")

    options: argparse.Namespace = parser.parse_args()
    logger.info("Welcome to %s!", sys.argv[0])

    for path in options.paths:
        if os.path.isfile(path):
            logger.debug("%s is a file", path)
            globs.filesToUse.append(path)
        else:
            logger.debug("%s is a directory", path)
            globs.dirsToUse.append(path)
    
    if not options.silent:
        app = App()
        app.SetAppName("stringFinder")
        app.SetAppDisplayName("stringFinder")

        from mainwindow import MainWindow
        wind = MainWindow()
        # app.SetTopWindow(wind)
        wind.Show()

        app.MainLoop()