#!/bin/bash
# wget a list of files in a text file
# Usage: ./wget_files.sh files.txt
while read line
do
	file=$line
	wget $file
	echo Finished downloading $file
done < $1
