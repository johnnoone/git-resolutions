#!/usr/bin/env python

import os.path
import subprocess
import sys
from .cli import parse_args
from ._version import get_versions

__all__ = ['install', 'publish']
__version__ = get_versions()['version']
del get_versions


def shell(*args, **kwargs):
    # sys.version_info
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    if args and isinstance(args[0], str):
        kwargs.setdefault('shell', True)
    proc = subprocess.Popen(*args, **kwargs)
    stdout, stderr = proc.communicate()
    if sys.version_info >= (3, 0, 0):
        stdout, stderr = stdout.decode('utf-8'), stderr.decode('utf-8')
    return proc, stdout.strip(), stderr.strip()


def install():
    directory = os.path.join('.git', 'rr-cache')

    # define origin
    proc, stdout, _ = shell(['git', 'config', 'remote.origin.url'])
    if proc.returncode:
        raise RuntimeError('Project has no origin')
    repository = stdout
    branch = 'rr-cache'

    # enable git-rerere
    shell(['git', 'config', 'rerere.enabled', 'true'])
    # implements versionning into rr-cache
    shell(['mkdir', '-p', directory])
    shell(['git', 'init'], cwd=directory)
    shell(['git', 'remote', 'add', 'origin', repository], cwd=directory)
    shell(['git', 'remote', 'set-url', 'origin', repository], cwd=directory)

    _, stdout, _ = shell(['git', 'symbolic-ref', '--short', 'HEAD'], cwd=directory)
    current_branch = stdout
    _, stdout, _ = shell(['git', 'branch'], cwd=directory)
    local_branches = stdout.split()

    proc, _, _ = shell(['git', 'ls-remote', '--exit-code', 'origin', branch], cwd=directory)

    if proc.returncode == 2:
        # branch does not exists on origin
        if current_branch == branch:
            # already on the good branch
            pass
        elif branch in local_branches:
            # checkout the good branch
            shell(['git', 'checkout', branch], cwd=directory)
        else:
            # must create branch
            shell(['git', 'checkout', '--orphan', branch], cwd=directory)
        shell('echo "enable git-conflict" > .gitkeep', cwd=directory)
        shell(['git', 'add', '.gitkeep'], cwd=directory)
        shell(['git', 'commit', '-m', 'enable git-conflict'], cwd=directory)
        shell(['git', 'push', '--set-upstream', 'origin', branch], cwd=directory)

    else:
        print('pull %s from origin' % branch)
        shell(['git', 'stash'], cwd=directory)
        if current_branch == branch:
            # already on the good branch
            shell(['git', 'pull', 'origin', branch, '--rebase'], cwd=directory)
        elif branch in local_branches:
            # checkout the good branch
            shell(['git', 'checkout', branch], cwd=directory)
            shell(['git', 'pull', 'origin', branch, '--rebase'], cwd=directory)
        else:
            # must create local branch
            track = 'origin/%s' % branch
            shell(['git', 'checkout', branch, '--track', track], cwd=directory)
        shell(['git', 'push', '--set-upstream', 'origin', branch], cwd=directory)
        shell(['git', 'stash', 'pop'], cwd=directory)


def publish():
    directory = os.path.join('.git', 'rr-cache')
    branch = 'rr-cache'
    _, stdout, _ = shell(['git', 'config', 'user.name'], cwd=directory)
    name = stdout
    _, stdout, _ = shell(['git', 'config', 'user.email'], cwd=directory)
    email = stdout
    message = 'pushed by %s <%s>' % (name, email)

    shell(['git', 'checkout', branch], cwd=directory)
    shell(['git', 'add', '-A'], cwd=directory)
    shell(['git', 'commit', '-m', message], cwd=directory)
    shell(['git', 'pull', 'origin', branch, '--rebase'], cwd=directory)
    shell(['git', 'push', 'origin', branch], cwd=directory)


def main():
    try:
        args, parser = parse_args()
        if args.action == 'install':
            install()
        elif args.action == 'publish':
            publish()
        else:
            raise ValueError('unknown action %s' % args.action)
    except Exception as error:
        parser.error(error)
