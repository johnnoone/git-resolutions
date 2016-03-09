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
      -l, --pull            pull resolutions from origin
      -p, --push            push resolutions to origin
      -f, --force           force command, even on mixmatch
      --directory DIRECTORY

Example::

    git merge origin/foo
    # resolve conflict merge
    git conflict --publish


How does it works?
~~~~~~~~~~~~~~~~~~

This command overlaps git-merge and git-rerere. .git/rr-cache directory will
be automatically created, and versionned in the origin/rr-cache branch.

To prepare the directory::

    git conflict --install

To fetch latest resolutions::

    git conflict --pull

To publish resolutions::

    git conflict --push
