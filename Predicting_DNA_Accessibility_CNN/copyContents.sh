#!/bin/bash

if [ "$#" -ne 2 ]; then
                echo "$0 source_folder to destination_folder needed"
                        exit 1
fi

source_folder=$1
destination_folder=$2

if [ ! -d "$source_folder" ]; then
                echo "Error opening $source_folder"
                        exit 1
fi


cp -r "$source_folder"/* "$destination_folder"

echo "copying of files is successful from $source_folder to $destination_folder successfully"