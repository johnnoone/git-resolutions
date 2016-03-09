git-conflict
------------

Handle rr-cache in your repository origin.

Usage::

  usage: git conflict --prepare | --publish | <commit-ish>

  publish merge resolutions

  positional arguments:
    commit-ish            commit-ish object names to merge

  optional arguments:
    -h, --help            show this help message and exit
    -i, --install         install git conflict
    -p, --publish         push resolutions to origin
    -f, --force           force command, even on mixmatch
    --directory DIRECTORY

Example::

    git merge origin/foo
    # resolve conflict merge
    git conflict --publish
