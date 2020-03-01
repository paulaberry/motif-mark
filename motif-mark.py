#!/usr/bin/env python3
import argparse
import gzip
import cairo
import re
import os
from matplotlib import imshow
import numpy as np

def get_args():
    """Function to pass in the FASTA file, motif list, and output options."""
    getfiles = argparse.ArgumentParser(description="A program to find and visually display motifs in genomes.")
    getfiles.add_argument("-f", "--fastafile", help = "FASTA file to be parsed", required = True)
    getfiles.add_argument("-m", "--motiffile", help = "file with list of motifs to mark", required = True)
    getfiles.add_argument("-c", "--colormap", help = "specifies which matplotlib color map to use for motifs (default: hsv)", required = False, default = "hsv")
    return getfiles.parse_args()
args = get_args()

# required arguments
fastafile = str(args.fastafile)
motiflist = str(args.motiffile)

# optional arguments
colormap = str(args.colormap)

# function to create dictionary values for motif keys
def values(motif):
    """Function to create dictionary value for motif key"""
    return regex_string(motif)
    # returns regex and symbol/color for each motif

def regex_string(motif):
    """Function that returns a regular expression string to search for in the sequence from a motif."""
    motifstring = motif.strip()
    value_regex = "(?i"
    for i in motifstring:
        if i == "T" or i == "t" or i == "U" or i == "u":
            value_regex = value_regex + "[TU]"
        elif i == "A" or i == "a":
            value_regex = value_regex + "[A]"
        elif i == "C" or i == "c":
            value_regex = value_regex + "[C]"
        elif i == "G" or i == "g":
            value_regex = value_regex + "[G]"
        elif i == "M" or i == "m":
            value_regex = value_regex + "[AC]"
        elif i == "R" or i == "r":
            value_regex = value_regex + "[AG]"
        elif i == "W" or i == "w":
            value_regex = value_regex + "[ATU]"
        elif i == "S" or i == "s":
            value_regex = value_regex + "[CG]"
        elif i == "Y" or i == "y":
            value_regex = value_regex + "[CTU]"
        elif i == "K" or i == "k":
            value_regex = value_regex + "[GTU]"
        elif i == "V" or i == "v":
            value_regex = value_regex + "[ACG]"
        elif i == "H" or i == "h":
            value_regex = value_regex + "[ACTU]"
        elif i == "D" or i == "d":
            value_regex = value_regex + "[AGTU]"
        elif i == "B" or i == "b":
            value_regex = value_regex + "[CGTU]"
        elif i == "N" or i == "n":
            value_regex = value_regex + "[AGCTUN]"
        else:
            value_regex = value_regex + i
    value_regex = value_regex + ")"
    return(value_regex)


# color values dictionary
def pick_colors(n, cmap):
    """A function that takes in as arguments the total number of motifs and the colormap desired and returns RGB values as tuples"""
    return cm.cmap(n)

# initialize motif dictionary
motif_dictionary = {}

# First input motifs, build dictionary
motif_file = open(motiflist, "r")
motif_count = 0
motif = motif_file.readline(0)
for motif in motif_file:
    motif = motif.strip()
    motif_dictionary[motif] = [regex_string(motif)]
    motif_count = motif_count + 1
motif_file.close()

# Populate dictionary with RGB value tuples
color_step = 255 % motif_count
color_n = 0
for key in motif_dictionary:
    motif_dictionary[key].append = pick_colors(color_n, cmap)
    color_n = color_n + color_step

print(motif_dictionary)



# Input FASTA file, count fasta entries
fasta_file = open(fastafile)
fasta_count = 0
fasta_line = fasta_file.readline(0)
for line in fasta_line:
    line = line.strip()
    if line.startswith == ">":
        fasta_count = fasta_count + 1
fasta_file.close()

print(fasta_count)

# Initialize canvas
#canvas_height = fasta_count * 100 + 100
#svg_filename = str(os.path.splitext(fastafile)[0]) + "_motifs.svg"
#with cairo.SVGSurface(svg_filename, 1100, canvas_height) as surface:
    #context = cairo.Context(surface)
# Loop here
    # input FASTA entry
        #Create single line FASTA

    # Initialize canvas, calculate each gene position on canvas
    # create labelfor the gene
    # search string
        # calculate length/position of exon(s)
    # search string
        # calculate position of motifs
    # draw gene and motifs
