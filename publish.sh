#!/bin/bash

rm -rf dist/ build/ *.egg-info/
python3 setup.py bdist_wheel
twine upload dist/*
