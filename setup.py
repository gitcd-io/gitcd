#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='gitcd',
    version='1.5.5',
    description='Tool for continuous delivery using git',
    author='Claudio Walser',
    author_email='claudio.walser@srf.ch',
    url='https://github.com/claudio-walser/gitcd',
    packages=find_packages(),
    install_requires=['pyyaml', 'argparse', 'argcomplete', 'requests'],
    entry_points={
        'console_scripts': [
            'git-cd = gitcd.__main__:main'
        ]
    },
    license = 'Apache License',
    keywords = ['git', 'application', 'continuos delivery'],
    classifiers = [
        'Development Status :: Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
    ]
)
