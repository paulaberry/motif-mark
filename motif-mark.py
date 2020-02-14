#!/usr/bin/env python3
import argparse

# We need to cound the reads in a SAM file to see if they are appropriately long.

def get_args():
    """Function to pass in the SAM file and options to remove PCR duplicates."""
    getfiles = argparse.ArgumentParser(description="A program to find and visually display motifs in genomes.")
    getfiles.add_argument("-f", "--fastafile", help = "FASTA file to be parsed", required = True)
    return getfiles.parse_args()
args = get_args()

# required arguments
filename = str(args.fastafile)
line_count = 0
total_bp = 0
sam_fh = open(str(args.fastafile), "r")
while True:
    line = sam_fh.readline()
    line = line.strip()
    if line == "":
        break
    elif line.startswith("@") == True:
        continue
    else:
        line = line.split()
        #print(line[9])
        length = len(line[9])
        total_bp = total_bp + length
        #print(total_bp)

print("The number of basepairs in " + str(args.samfile) + " is: " + str(total_bp))

sam_fh.close()
