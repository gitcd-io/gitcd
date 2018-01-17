#!/usr/bin/env python3

from setuptools import setup, find_packages


def read(fpath):
    with open(fpath, 'r') as f:
        return f.read()


def version(fpath):
    return read(fpath).strip()


setup(
    name='gitcd',
    version=version('version.txt'),
    description='Tool for continuous delivery using git',
    long_description=read('README.rst'),
    author='Claudio Walser',
    author_email='claudio.walser@srf.ch',
    url='https://github.com/claudio-walser/gitcd',
    packages=find_packages(),
    install_requires=[
        'simpcli',
        'pyyaml',
        'argparse',
        'argcomplete',
        'requests',
        'packaging',
        'kivy',
        'KivyMD'
    ],
    dependency_links=[
        'git+https://gitlab.com/kivymd/KivyMD@master#egg=KivyMD'
    ],

    entry_points={
        'console_scripts': [
            'git-cd = gitcd.bin.console:main',
            'git-cd-ui = gitcd.bin.kivy:main',
        ]
    },
    license='Apache License',
    keywords=['git', 'application', 'continuos delivery'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ]
)
