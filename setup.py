#!/usr/bin/env python3

from setuptools import setup

setup(
    name='gitcd',
    version='1.1.0',
    description='Tool for continous delivery using git',
    author='Claudio Walser',
    author_email='claudio.walser@srf.ch',
    url='https://github.com/claudio-walser/gitcd',
    packages = ['.', 'gitcd', 'gitcd.Cli','gitcd.Config','gitcd.Git'],
    install_requires=['pyyaml', 'argcomplete', 'requests'],
    entry_points={
        'console_scripts': [
            'my_project = gitcd.__main__:main'
        ]
    }
)
