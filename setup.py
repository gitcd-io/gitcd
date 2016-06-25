#!/usr/bin/env python

from setuptools import setup

setup(name='gitcd',
      version='1.0.3',
      description='Tool for continous delivery using git',
      author='Claudio Walser',
      author_email='claudio.walser@srf.ch',
      url='https://github.com/claudio-walser/gitcd',
      packages=['gitcd'],
      install_requires=['pyyaml', 'argcomplete']
)