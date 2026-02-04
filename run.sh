#!/bin/bash

# Ensure UTF-8 encoding (equivalent of chcp 65001)
export LANG=en_US.UTF-8

# Create folders if they don't exist
mkdir -p ./Backup ./In ./Out

# Loop to read the number of table states (n)
while true; do
    read -p "Enter the number of table states to generate: " n
    # Remove spaces
    n=$(echo "$n" | tr -d ' ')
    
    # Check it's a non-negative integer
    if [[ "$n" =~ ^[0-9]+$ ]]; then
        break
    else
        echo "Please enter a non-negative integer."
    fi
done

# Loop to read the weight (w)
while true; do
    read -p "Enter the weight (non-negative real number): " w
    # Remove spaces
    w=$(echo "$w" | tr -d ' ')
    
    # Check it's a real number (e.g., 2 or 2.5)
    if [[ "$w" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
        break
    else
        echo "Please enter a non-negative real number."
    fi
done

echo "Running the main script"
# Use python3, the standard on Linux/macOS
python3 main.py "$n" "$w"

echo "Creating the report and adding it to the Backup directory"
python3 backup_script.py

echo "Opening the latest report"
# Choose the appropriate command to open the file based on the system
if [[ "$OSTYPE" == "darwin"* ]]; then
    open LastRaport.html  # macOS
else
    xdg-open LastRaport.html 2>/dev/null || echo "Could not open browser automatically." # Linux
fi

read -p "Press Enter to continue..."