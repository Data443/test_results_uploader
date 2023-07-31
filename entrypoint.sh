#!/bin/bash

# Execute the Python script and capture the output
output=$(python main.py "$1" "$2")

# Print the captured output
echo "$output"
