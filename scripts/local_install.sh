#!/usr/bin/env bash

pip uninstall tensortime -y

python setup.py clean
python setup.py install
