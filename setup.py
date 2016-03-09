#!/usr/bin/env python

from setuptools import setup
import versioneer

setup(
    name='git-conflict',
    version=versioneer.get_version(),
    package_dir={'': 'src'},
    cmdclass=versioneer.get_cmdclass()
)
