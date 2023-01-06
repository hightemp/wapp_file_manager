#!/bin/bash

# nuitka3 --standalone --onefile main.py

# # pyinstaller -F main.py
# # # cp dist/main wapp_file_manager

# exit

# # https://stackoverflow.com/questions/39913847/is-there-a-way-to-compile-a-python-application-into-static-binary
# PY=python3
# CPY=cython
# $CPY main.py --embed
# PYTHONLIBVER=python$($PY -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')$($PY-config --abiflags)
# gcc -Os $($PY-config --includes) main.c -o wapp_file_manager $($PY-config --ldflags) -l$PYTHONLIBVER

CFILE=wapp_file_manager

if [ "$1" == "" ]; then
    pyinstaller -F --path "." --add-data "templates:templates" --add-data "static:static" --hidden-import "main" --hidden-import "baselib" --hidden-import "database" --hidden-import "request_vars" __main__.py
    cp dist/__main__ ../$CFILE
    cd ..
    $CFILE  --bind 0.0.0.0:5021
elif [ "$1" == "zipapp" ]; then
    # cp .env ..
    cd ..
    python3 -m zipapp $CFILE -p "/usr/bin/env python3"
    rm ./$CFILE.database.db
    echo $PWD/$CFILE.pyz
    ./$CFILE.pyz --bind 0.0.0.0:5000 -w 10
fi
