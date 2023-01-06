#!/bin/bash

timestamp=$(date +%s)
VERSION=$(echo `cat VERSION`.$timestamp)

git add .
git commit -am "`date` update"
git tag $VERSION
git push

if [ "$?" != "0" ]; then
    echo "====================================================="
    echo "ERROR"
    echo
    exit 1
fi

echo "[!] " gh release create $VERSION -t $VERSION -n '""' --target main
gh release create $VERSION -t $VERSION -n "" --target main

CFILE=wapp_file_manager

# rm ../$CFILE.pyz
# ./build.sh zipapp
# if [ -f ../$CFILE.pyz ]; then
#     gh release upload $VERSION ../$CFILE.pyz --clobber
# fi

rm ../$CFILE.bin
./build.sh pyinst_docker
if [ -f ../$CFILE.bin ]; then
    gh release upload $VERSION ../$CFILE.bin --clobber
fi

# mv wapp_file_manager.pyz ./wapp_file_manager
# cd wapp_file_manager

# echo gh release create $VERSION -t $VERSION -n '""' $CFILE
# gh release create $VERSION -t $VERSION -n "" $CFILE