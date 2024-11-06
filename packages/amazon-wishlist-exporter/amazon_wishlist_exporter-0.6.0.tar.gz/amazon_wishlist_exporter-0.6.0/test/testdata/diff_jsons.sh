#!/bin/bash

# Define the directories
dir1="json_from_url"
dir2="json_from_html"

# Find all the .json files in the first directory (json_from_url)
for file1 in "$dir1"/*.json; do
    # Extract the filename (without path) from the first directory
    filename=$(basename "$file1")

    # Check if the corresponding file exists in the second directory
    file2="$dir2/$filename"
    if [[ -f "$file2" ]]; then
        # Show the diff between the two files
        echo "Showing diff for: $filename"
        diff -uiw "$file1" "$file2" | batcat

        # Wait for the user to press any key before continuing
        read -n 1 -s -r -p "Press any key to continue to the next diff..."
        echo # newline for better formatting
    else
        echo "No matching file for: $filename in $dir2"
    fi
done
