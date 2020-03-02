#!/usr/bin/env python3
import argparse
import cairo
import re
import os
from matplotlib import cm

def get_args():
    """Function to pass in the FASTA file, motif list, and output options."""
    getfiles = argparse.ArgumentParser(description="A program to find and visually display motifs in genomes.")
    getfiles.add_argument("-f", "--fastafile", help = "FASTA file to be parsed", required = True)
    getfiles.add_argument("-m", "--motiffile", help = "file with list of motifs to mark", required = True)
    getfiles.add_argument("-c", "--colormap", help = "specifies which matplotlib color map to use for motifs (default: hsv)", required = False, default = "hsv")
    getfiles.add_argument("-o", "--output", help = "specifies output filetype (default:svg)", required = False, default = "svg")
    return getfiles.parse_args()
args = get_args()

# required arguments
fastafile = str(args.fastafile)
motiflist = str(args.motiffile)

# optional arguments
colormap = str(args.colormap)
filetype = str(args.output)
if filetype.startswith(".") == False:
    filetype = "." + filetype

def regex_string(motif):
    """Function that returns a regular expression string to search for in the sequence from a motif."""
    motifstring = motif.strip()
    value_regex = "(?i)"
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
    return(value_regex)

def exonlength(sequence):
    """A function that takes in a FASTA sequence as a string and returns the coordinates for the exon start and stop"""
    m = re.search("[A-Z]+", sequence)
    ex_start = int((m.start() / len(sequence)) * 1000)
    ex_end = int((m.end() / len(sequence)) * 1000)
    return ex_start, ex_end

def motif_location(motif, sequence, dictionary):
    """A function that takes in a motif, a FASTA sequence as a string, and an empty list to populate with the coordinates of the motif found."""
    coord_list = []
    p = re.compile(dictionary[motif][0])
    for match in p.finditer(sequence):  # Search for the motif in the sequence
        coord_list.append(match.start())
    if coord_list == []: # if no matches for the motif
        return coord_list
    else:
        list_count = 0
        for i in coord_list:
            scaled_coord = int((i / len(sequence)) * 1000)
            coord_list[list_count] = scaled_coord
            list_count = list_count + 1
        return coord_list

def fasta_process(fasta, dictionary):
    """A function that takes in a fasta file object, and an empty dictionary, and populates the dictionary with the fasta headers as keys and a list of the fasta sequence and a scalar as the value. Returns the count of fasta files"""
    fasta_file = open(fasta, "r")
    sequence =""
    counter = 0
    for line in fasta_file:
        line = line.strip()
        if counter == 0: # special case for first loop through
            header = line[1:]
            dictionary[header] = []
            counter = counter + 1

        elif line[0] == ">": # this works for all except very first one
            dictionary[header].append(sequence) # as soon as hit the next header line store sequence in previous header value
            sequence = "" # clear the sequence
            header = line[1:]
            dictionary[header] = [] # store the next header as a key
            counter = counter + 1

        else: # build the sequence
            sequence = sequence + line

    dictionary[header].append(sequence) # store the last sequence
    fasta_file.close()

    # Find scalars for sequences
    max_seq = 0
    for i in dictionary:
        dictionary[i].append(len(dictionary[i][0]))
        max_seq = max(dictionary[i][1], max_seq)
    for i in dictionary:
        dictionary[i][1] = dictionary[i][1] / max_seq


    return len(dictionary)



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
color_step = int(255 / motif_count)
color_n = 0
for key in motif_dictionary:
    motif_dictionary[key].append(getattr(cm, colormap)(color_n))
    color_n = color_n + color_step

# Input FASTA file, count fasta entries
fasta_dict = {}
fasta_count = fasta_process(fastafile, fasta_dict)

# Initialize canvas
canvas_height = (fasta_count * 100) + 160 + (30 * motif_count)
img_filename = str(os.path.splitext(fastafile)[0]) + "_motifs" + filetype

with cairo.SVGSurface(img_filename, 1100, canvas_height) as surface:
    context = cairo.Context(surface)
    context.set_source_rgb(0, 0, 0)
    context.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL,
        cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(13)
    context.move_to(20, 30)
    context.show_text("Motif Legend")
    legend_line = 30
    for key in motif_dictionary: # create legend with all motifs and colors
        legend_line = legend_line + 30
        context.set_source_rgb(motif_dictionary[key][1][0], motif_dictionary[key][1][1], motif_dictionary[key][1][2])
        context.rectangle(20, (legend_line-15), 50, 20)
        context.fill()
        context.set_source_rgb(0, 0, 0)
        context.move_to(80, legend_line)
        context.show_text(key)

    draw_line = legend_line + 100 # start the diagrams 100 pixels below the legend
    for key in fasta_dict:
        header = key
        sequence = fasta_dict[key][0]
        exon_start, exon_stop = exonlength(sequence) # generate coordinates for exon(s)

        # draw using the coordinates
        draw_strand = int(draw_line + 30)
        context.set_source_rgb(0, 0, 0)
        context.move_to(20, draw_line)
        context.show_text(header) # draw gene text label
        context.move_to(50, draw_strand)
        context.line_to(int(50 + (fasta_dict[key][1] * 1000)), draw_strand)
        context.set_source_rgba(0, 0, 0, .7)
        context.set_line_width(5)
        context.stroke() # draw whole sequence span
        context.move_to(50 + int(fasta_dict[key][1] * exon_start), draw_strand)
        context.line_to(50 + int(fasta_dict[key][1] * exon_stop), draw_strand)
        context.set_source_rgb(0, 0, 0)
        context.set_line_width(20)
        context.stroke() # draw exon(s)

        # generate list of motif coordinates
        for x in motif_dictionary:
            motif_len = int((len(x) / len(sequence)) * 1000 * fasta_dict[key][1])
            motif_coords = motif_location(x, sequence, motif_dictionary)
            if motif_coords != []:
                for i in motif_coords:
                    context.move_to(50 + int(i * fasta_dict[key][1]), draw_strand)
                    context.line_to(50 + int(i * fasta_dict[key][1]) + motif_len, draw_strand)
                    context.set_source_rgba(motif_dictionary[x][1][0], motif_dictionary[x][1][1], motif_dictionary[x][1][2], 1)
                    context.set_line_width(20)
                    context.stroke()


        draw_line = draw_line + 100
surface.finish()
