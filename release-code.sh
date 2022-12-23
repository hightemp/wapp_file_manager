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

# CFILE=wapp_file_manager.pyz

cd ..
python3 -m zipapp wapp_file_manager -p "/usr/bin/env python3"
echo $PWD/wapp_file_manager.pyz
cd wapp_file_manager
gh release upload $VERSION ../wapp_file_manager.pyz --clobber

# mv wapp_file_manager.pyz ./wapp_file_manager
# cd wapp_file_manager

# echo gh release create $VERSION -t $VERSION -n '""' $CFILE
# gh release create $VERSION -t $VERSION -n "" $CFILE