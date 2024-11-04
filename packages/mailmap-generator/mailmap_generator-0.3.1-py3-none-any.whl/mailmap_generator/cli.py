"""
This program creates a `.mailmap` file from the authors that contributed to a
Git repository.

Authors with different names but same email addresses are automatically mapped
to the first name that occurs and names that are the same but with different
email addresses are also mapped to each other.

That is, the generated `mailmap` may map different users with same names to
each other. Therefore, inspect and manually edit the generated file before use.

Usage:
  mailmap <repository>...
  mailmap -h | --help
  mailmap --version

Options:
  -h --help             Show this screen.
  --version             Show version.
"""

import sys
from shutil import which
from docopt import docopt
from mailmap_generator import __version__
from mailmap_generator.mailmap import create_mailmap, git_is_available


def main():
    if not git_is_available():
        print("mailmap requires `git` to be installed and accessible on path", file=sys.stderr)
        sys.exit(1)
    arguments = docopt(__doc__, version=__version__)
    paths_to_repos = arguments["<repository>"]
    mailmap_str = create_mailmap(paths_to_repos)
    print(mailmap_str)


if __name__ == "__main__":
    main()
