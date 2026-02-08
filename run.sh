#!/bin/bash

export LANG=en_US.UTF-8

mkdir -p ./Backup ./In ./Out

while true; do
    read -p "Enter the number of table states to generate: " n
    n=$(echo "$n" | tr -d ' ')
    
    if [[ "$n" =~ ^[0-9]+$ ]]; then
        break
    else
        echo "Please enter a non-negative integer."
    fi
done

while true; do
    read -p "Enter the weight (non-negative real number): " w
    w=$(echo "$w" | tr -d ' ')
    
    if [[ "$w" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
        break
    else
        echo "Please enter a non-negative real number."
    fi
done

echo "Running the main script"
python3 main.py "$n" "$w"

echo "Creating the report and adding it to the Backup directory"
python3 backup_script.py

echo "Opening the latest report"
if [[ "$OSTYPE" == "darwin"* ]]; then
    open LastRaport.html  # macOS
else
    xdg-open LastRaport.html 2>/dev/null || echo "Could not open browser automatically." # Linux
fi

read -p "Press Enter to continue..."