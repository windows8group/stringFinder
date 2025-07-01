# stringFinder

A tool to find localizable strings and maybe, apply them to your code.

## Usage

Requires Python 3.1x.

stringFinder has both GUI and CLI. For CLI, use `--help` to see all available things to set. For GUI, check the menu bar.

Specify input files and/or folders, also output folder.

No specialization for input things, but for output folders:

* They must be made to contain sub folders whose name a language code;
* Has enough read-write permission of course
* A name for resource files will be used globally, defaults to `Resources`.

You are always able to override the list of languages to be generated/read.

Upon output folder selection, if the target languages list is empty, stringFinder will find for languages itself by scanning the selected output location.

### Settings

All are placed in `~/.stringFinder/settings.json`.
