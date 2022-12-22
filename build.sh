#!/bin/bash

pyinstaller -F main.py
# cp dist/main wapp_file_manager

exit

# https://stackoverflow.com/questions/39913847/is-there-a-way-to-compile-a-python-application-into-static-binary
PY=python38
CPY=cython
$CPY main.py --embed
PYTHONLIBVER=python$($PY -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')$($PY-config --abiflags)
gcc -Os $($PY-config --includes) main.c -o wapp_file_manager $($PY-config --ldflags) -l$PYTHONLIBVER

