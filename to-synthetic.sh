#!/bin/bash

set -e

# Source file and destination directory (hardcoded names)
SRC_FILE="./resources.json"
DEST_DIR="../ltoscano.github.io/data/resources"

# Check if the source file exists
if [[ ! -f "$SRC_FILE" ]]; then
    echo "Source file not found: $SRC_FILE"
    exit 1
fi

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Copy the file to the destination directory
cp "$SRC_FILE" "$DEST_DIR"

echo "File $SRC_FILE copied to $DEST_DIR"
