#!/usr/bin/env python3

import subprocess
import os
import argparse

'''
OPS445 Assignment 2 - Winter 2022
Program: duim.py 
Author: Vikas Durani
The python code in this file (duim.py) is original work written by
Vikas Durani. No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This script visualizes disk usage of a directory using a bar chart. It uses the `du` command and draws proportional bars for each subdirectory.

Date: 2025-04-08
'''

def parse_command_args():
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts", epilog="Copyright 2025")
    parser.add_argument("-H", "--human-readable", action="store_true", help="Show sizes in human readable format")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("target", type=str, nargs="?", default=".", help="Target directory to analyze (default is current directory)")
    return parser.parse_args()


def percent_to_graph(percent, total_chars):
    hashes = round((percent / 100) * total_chars)
    return '#' * hashes + ' ' * (total_chars - hashes)


def call_du_sub(location):
    try:
        result = subprocess.run(['du', '-d', '1', location], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        print(f"Error running du: {e}")
        return []


def create_dir_dict(alist):
    result = {}
    for line in alist:
        if '\t' in line:
            size_str, path = line.split('\t')
        else:
            size_str, path = line.split(maxsplit=1)
        result[path.strip()] = int(size_str)
    return result


def to_human_readable(kb):
    if kb > 1024 * 1024:
        return f"{kb / (1024 * 1024):.1f}G"
    elif kb > 1024:
        return f"{kb / 1024:.1f}M"
    else:
        return f"{kb}K"


if __name__ == "__main__":
    # Parse the command-line arguments
    args = parse_command_args()
    target = args.target  # Get the target directory (default is current directory)

    # Check if the provided target directory is valid
    if not os.path.isdir(target):
        print(f"Error: {target} is not a valid directory.")
        exit(1)

    # Call 'du' on the target directory and get the result
    data = call_du_sub(target)

    # If no data was returned, print an error and exit
    if not data:
        print("No data returned. Exiting.")
        exit(1)

    # Create a dictionary of directories and their sizes
    dir_dict = create_dir_dict(data)

    # Calculate the total size of the target directory
    total_size = sum(dir_dict.values())

    # Print the sizes for each subdirectory with a graph
    print(f"Disk Usage for: {target}\n")
    for path, size in sorted(dir_dict.items(), key=lambda x: x[1], reverse=True):
        # Skip the target directory itself
        if path == target:
            continue

        # Calculate the percentage of total size
        percent = (size / total_size) * 100

        # Create the bar graph
        bar = percent_to_graph(percent, args.length)

        # Print the human-readable size or raw size based on the argument
        size_str = to_human_readable(size) if args.human_readable else f"{size}K"

        # Print the result
        print(f"{percent:.1f}% {bar} {size_str} {path}")

