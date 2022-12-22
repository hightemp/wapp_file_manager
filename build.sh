#!/bin/bash

# https://stackoverflow.com/questions/39913847/is-there-a-way-to-compile-a-python-application-into-static-binary
cython main.py --embed
PYTHONLIBVER=python$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')$(python3-config --abiflags)
gcc -Os $(python3-config --includes) main.c -o wapp_file_manager $(python3-config --ldflags) -l$PYTHONLIBVER

