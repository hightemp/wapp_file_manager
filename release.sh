# CFILE=wapp_file_manager
CFILE=./dist/main

./build.sh

if [ "$?" != "0" ]; then
    echo "====================================================="
    echo "ERROR"
    echo
    exit 1
fi

strip -s ./$CFILE

if [ "$?" != "0" ]; then
    echo "====================================================="
    echo "ERROR"
    echo
    exit 1
fi

# upx --best ./$CFILE

# if [ "$?" != "0" ]; then
#     echo "====================================================="
#     echo "ERROR"
#     echo
#     exit 1
# fi

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

echo gh release create $VERSION -t $VERSION -n '""' $CFILE
gh release create $VERSION -t $VERSION -n "" $CFILE