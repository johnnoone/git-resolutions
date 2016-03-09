git-conflict
------------

Handle rr-cache in your repository origin.

Usage::

  usage: git conflict --prepare | --publish | <commit-ish>

  publish merge resolutions

  optional arguments:
    -h, --help  show this help message and exit
    --install   install git conflict
    --publish   publish rr-cache to origin

Example::

    git merge origin foo
    # resolve conflict merge
    git conflict --publish
