# What is this?

This tool, `mailmap-generator` suggests a Git `.mailmap` file based on the commit history.
It is intended to support you when you have a repository for which you do not have a `.mailmap` file yet but want to create one.


## Installation

```
pip install mailmap-generator
```

### Requirements

The tool requires that `git` is installed and accessible on `PATH`.


## How to use it?

You have to either point the tool to a directory containing a Git repository.
From the terminal, the tool can be run as in the following:

```
Usage:
  mailmap <repository>
  mailmap -h | --help
  mailmap --version

Options:
  -h --help             Show this screen.
  --version             Show version.
```

For example, if you wanted to create a `.mailmap` file for the `psf/requests` repository, it could be done as in the following:


```bash
$ git clone https://github.com/psf/requests
$ mailmap requests > requests/.mailmap
$ nano requests/.mailmap
```

The above shows, that the tool just prints a suggested `.mailmap` file to stdout. Be aware of that the tool only _suggests_ a `.mailmap` file.
It might be wrong. Since the tool maps same author names, you have to inspect and double check if the suggested file is correct.


Calling it from code:

```python
from mailmap_generator.mailmap import create_mailmap

mailmap_str = create_mailmap(["<path_to_repo>", ... ])
```


## How does the tool create the `.mailmap` file?

Currently, the tool works in two stages. In the first stage, authors with the same email address are mapped to one author name. Secondly, all authors with the exact same name -- and potentially different email addresses -- are mapped to another. That second step might be wrong in case of authors with same names but different email addresses are actually two different persons.

## Alternative tools

Via [StackOverflow](https://stackoverflow.com/questions/6502018/tool-to-automate-building-a-mailmap-file) one finds [`genmailmap.sh`](https://github.com/greenrd/genmailmap/blob/master/genmailmap.sh) and [`mailmap_update.py`](https://github.com/sympy/sympy/blob/181d1e630e248c46917a18e9e9fc1cf0990dff6f/bin/mailmap_update.py). The latter is removed from the project, i.e., not maintained anymore and inner workings of the former is not entirely clear to me :) Therefore, I created this tool.