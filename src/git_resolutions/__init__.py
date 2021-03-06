#!/usr/bin/env python

import os.path
import subprocess
import sys
from .cli import parse_args
from ._version import get_versions

__all__ = ['install', 'publish', 'check']
__version__ = get_versions()['version']
del get_versions


def shell(*args, **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    if args and isinstance(args[0], str):
        kwargs.setdefault('shell', True)
    proc = subprocess.Popen(*args, **kwargs)
    stdout, stderr = proc.communicate()

    if kwargs['stdout'] == subprocess.PIPE:
        if sys.version_info >= (3, 0, 0):
            # convert bytes to str
            stdout = stdout.decode('utf-8')
        stdout = stdout.strip()

    if kwargs['stderr'] == subprocess.PIPE:
        if sys.version_info >= (3, 0, 0):
            # convert bytes to str
            stderr = stderr.decode('utf-8')
        stderr = stderr.strip()

    return proc, stdout, stderr


def install(directory=None, force=False):
    cache_dir = os.path.join(directory or '.', '.git', 'rr-cache')

    # define origin
    proc, stdout, _ = shell(['git', 'config', 'remote.origin.url'], cwd=directory)
    if proc.returncode:
        raise RuntimeError('Project has no origin')
    repository = stdout
    branch = 'rr-cache'

    # enable git-rerere
    shell(['git', 'config', 'rerere.enabled', 'true'], cwd=directory)
    # implements versionning into rr-cache
    shell(['mkdir', '-p', cache_dir])
    shell(['git', 'init'], cwd=cache_dir)
    shell(['git', 'config', 'rerere.enabled', 'false'], cwd=cache_dir)

    _, stdout, _ = shell(['git', 'config', 'remote.origin.url'], cwd=cache_dir)
    orig = stdout
    if orig == repository:
        # do nothing
        pass
    elif not orig:
        # track nothing
        shell(['git', 'remote', 'add', 'origin', repository], cwd=cache_dir)
    elif force:
        # track the real origin "warning!!!"
        shell(['git', 'remote', 'set-url', 'origin', repository], cwd=cache_dir)
    else:
        raise RuntimeError('Project and %s track different origins' % cache_dir)

    _, stdout, _ = shell(['git', 'symbolic-ref', '--short', 'HEAD'], cwd=cache_dir)
    current_branch = stdout
    _, stdout, _ = shell(['git', 'branch'], cwd=cache_dir)
    local_branches = stdout.split()

    proc, _, _ = shell(['git', 'ls-remote', '--exit-code', 'origin', branch], cwd=cache_dir)

    if proc.returncode == 2:
        # branch does not exists on origin
        if current_branch == branch:
            # already on the good branch
            pass
        elif branch in local_branches:
            # checkout the good branch
            shell(['git', 'checkout', branch], cwd=cache_dir)
        else:
            # must create branch
            shell(['git', 'checkout', '--orphan', branch], cwd=cache_dir)
        shell('echo "enable git-resolutions" > .gitkeep', cwd=cache_dir)
        shell(['git', 'add', '.gitkeep'], cwd=cache_dir)
        shell(['git', 'commit', '-m', 'enable git-resolutions'], cwd=cache_dir)
        shell(['git', 'push', '--set-upstream', 'origin', branch], cwd=cache_dir)

    else:
        shell(['git', 'stash'], cwd=cache_dir)
        if current_branch == branch:
            # already on the good branch
            shell(['git', 'pull', 'origin', branch, '--rebase'], cwd=cache_dir)
        elif branch in local_branches:
            # checkout the good branch
            shell(['git', 'checkout', branch], cwd=cache_dir)
            shell(['git', 'pull', 'origin', branch, '--rebase'], cwd=cache_dir)
        else:
            # must create local branch
            track = 'origin/%s' % branch
            proc, _, _ = shell(['git', 'checkout', '-b', branch, '--track', track], cwd=cache_dir)
            if proc.returncode:
                # something failed, try with a simple checkout
                proc, _, _ = shell(['git', 'checkout', '-b', branch], cwd=cache_dir)
            if not proc.returncode:
                # we can consider now that we have switched to the good branch
                current_branch = branch
        shell(['git', 'push', '--set-upstream', 'origin', branch], cwd=cache_dir)
        shell(['git', 'stash', 'pop'], cwd=cache_dir)


def fetch(directory=None):
    cache_dir = os.path.join(directory or '.', '.git', 'rr-cache')
    branch = 'rr-cache'

    # Prerequisite checks
    check(directory)
    shell(['git', 'pull', 'origin', branch, '--rebase'], cwd=cache_dir)


def publish(directory=None):
    cache_dir = os.path.join(directory or '.', '.git', 'rr-cache')
    branch = 'rr-cache'

    # Prerequisite checks
    check(directory)

    _, stdout, _ = shell(['git', 'config', 'user.name'], cwd=cache_dir)
    name = stdout
    _, stdout, _ = shell(['git', 'config', 'user.email'], cwd=cache_dir)
    email = stdout
    message = 'pushed by %s <%s>' % (name, email)

    shell(['git', 'checkout', branch], cwd=cache_dir)
    shell(['git', 'add', '-A'], cwd=cache_dir)
    shell(['git', 'commit', '-m', message], cwd=cache_dir)
    shell(['git', 'pull', 'origin', branch, '--rebase'], cwd=cache_dir)
    shell(['git', 'push', 'origin', branch], cwd=cache_dir)


def merge(directory=None, ref=None):
    if ref is None:
        raise RuntimeError('reference is required')
    fetch(directory)
    # TODO handle merge here
    proc, _, _ = shell(['git', 'merge', ref], stdout=None, stderr=None, cwd=directory)
    if proc.returncode:
        return False
    publish(directory)


def check(directory=None):
    cache_dir = os.path.join(directory or '.', '.git', 'rr-cache')
    branch = 'rr-cache'

    if not os.path.isfile(os.path.join(cache_dir, '.git', 'config')):
        raise RuntimeError('%s is not versionned' % cache_dir)
    _, stdout, _ = shell(['git', 'config', 'remote.origin.url'], cwd=cache_dir)
    orig = stdout
    if not orig:
        raise RuntimeError('%s does not track origin' % cache_dir)
    _, stdout, _ = shell(['git', 'config', 'remote.origin.url'], cwd=directory)
    if orig != stdout:
        raise RuntimeError('Project and %s track different repositories' % cache_dir)

    _, stdout, _ = shell(['git', 'symbolic-ref', '--short', 'HEAD'], cwd=cache_dir)
    current_branch = stdout
    if current_branch != branch:
        raise RuntimeError('%s does point to origin/%s but %s' % (cache_dir, branch, current_branch))


def main():
    try:
        args, parser = parse_args()
        if args.action == 'install':
            response = install(args.directory, args.force)
        elif args.action == 'publish':
            response = publish(args.directory)
        elif args.action == 'fetch':
            response = fetch(args.directory)
        elif args.action == 'merge':
            response = merge(args.directory, args.ref)
        else:
            raise ValueError('unknown action %s' % args.action)
    except Exception as error:
        parser.error(error)
    parser.exit(1 if response is False else 0)
