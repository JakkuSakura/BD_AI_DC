#!/bin/sh
for file in ./*.py
do
    echo Uploading $file
    ./ampy.sh put $file
done
