#!/usr/bin/env python3
import argparse
import cairo
import re
from matplotlib import cm

def get_args():
    """Function to pass in the FASTA file, motif list, and output options."""
    getfiles = argparse.ArgumentParser(description="A program to find and visually display motifs in genomes.")
    getfiles.add_argument("-f", "--fastafile", help = "FASTA file to be parsed", required = True)
    getfiles.add_argument("-m", "--motiffile", help = "file with list of motifs to mark", required = True)
    getfiles.add_argument("-c", "--colormap", help = "specifies which matplotlib color map to use for motifs (default: jet)", required = False, default = "jet")
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

# custom color options
custom_colors = {'aliceblue': (0.9411764705882353, 0.9725490196078431, 1.0), 'antiquewhite': (0.9803921568627451, 0.9215686274509803, 0.8431372549019608), 'aqua': (0.0, 1.0, 1.0), 'aquamarine': (0.4980392156862745, 1.0, 0.8313725490196079), 'azure': (0.9411764705882353, 1.0, 1.0), 'beige': (0.9607843137254902, 0.9607843137254902, 0.8627450980392157), 'bisque': (1.0, 0.8941176470588236, 0.7686274509803922), 'black': (0.0, 0.0, 0.0), 'blanchedalmond': (1.0, 0.9215686274509803, 0.803921568627451), 'blue': (0.0, 0.0, 1.0), 'blueviolet': (0.5411764705882353, 0.16862745098039217, 0.8862745098039215), 'brown': (0.6470588235294118, 0.16470588235294117, 0.16470588235294117), 'burlywood': (0.8705882352941177, 0.7215686274509804, 0.5294117647058824), 'cadetblue': (0.37254901960784315, 0.6196078431372549, 0.6274509803921569), 'chartreuse': (0.4980392156862745, 1.0, 0.0), 'chocolate': (0.8235294117647058, 0.4117647058823529, 0.11764705882352941), 'coral': (1.0, 0.4980392156862745, 0.3137254901960784), 'cornflowerblue': (0.39215686274509803, 0.5843137254901961, 0.9294117647058824), 'cornsilk': (1.0, 0.9725490196078431, 0.8627450980392157), 'crimson': (0.8627450980392157, 0.0784313725490196, 0.23529411764705882), 'cyan': (0.0, 1.0, 1.0), 'darkblue': (0.0, 0.0, 0.5450980392156862), 'darkcyan': (0.0, 0.5450980392156862, 0.5450980392156862), 'darkgoldenrod': (0.7215686274509804, 0.5254901960784314, 0.043137254901960784), 'darkgray': (0.6627450980392157, 0.6627450980392157, 0.6627450980392157), 'darkgreen': (0.0, 0.39215686274509803, 0.0), 'darkgrey': (0.6627450980392157, 0.6627450980392157, 0.6627450980392157), 'darkkhaki': (0.7411764705882353, 0.7176470588235294, 0.4196078431372549), 'darkmagenta': (0.5450980392156862, 0.0, 0.5450980392156862), 'darkolivegreen': (0.3333333333333333, 0.4196078431372549, 0.1843137254901961), 'darkorange': (1.0, 0.5490196078431373, 0.0), 'darkorchid': (0.6, 0.19607843137254902, 0.8), 'darkred': (0.5450980392156862, 0.0, 0.0), 'darksalmon': (0.9137254901960784, 0.5882352941176471, 0.47843137254901963), 'darkseagreen': (0.5607843137254902, 0.7372549019607844, 0.5607843137254902), 'darkslateblue': (0.2823529411764706, 0.23921568627450981, 0.5450980392156862), 'darkslategray': (0.1843137254901961, 0.30980392156862746, 0.30980392156862746), 'darkslategrey': (0.1843137254901961, 0.30980392156862746, 0.30980392156862746), 'darkturquoise': (0.0, 0.807843137254902, 0.8196078431372549), 'darkviolet': (0.5803921568627451, 0.0, 0.8274509803921568), 'deeppink': (1.0, 0.0784313725490196, 0.5764705882352941), 'deepskyblue': (0.0, 0.7490196078431373, 1.0), 'dimgray': (0.4117647058823529, 0.4117647058823529, 0.4117647058823529), 'dimgrey': (0.4117647058823529, 0.4117647058823529, 0.4117647058823529), 'dodgerblue': (0.11764705882352941, 0.5647058823529412, 1.0), 'firebrick': (0.6980392156862745, 0.13333333333333333, 0.13333333333333333), 'floralwhite': (1.0, 0.9803921568627451, 0.9411764705882353), 'forestgreen': (0.13333333333333333, 0.5450980392156862, 0.13333333333333333), 'fuchsia': (1.0, 0.0, 1.0), 'gainsboro': (0.8627450980392157, 0.8627450980392157, 0.8627450980392157), 'ghostwhite': (0.9725490196078431, 0.9725490196078431, 1.0), 'gold': (1.0, 0.8431372549019608, 0.0), 'goldenrod': (0.8549019607843137, 0.6470588235294118, 0.12549019607843137), 'gray': (0.5019607843137255, 0.5019607843137255, 0.5019607843137255), 'green': (0.0, 0.5019607843137255, 0.0), 'greenyellow': (0.6784313725490196, 1.0, 0.1843137254901961), 'grey': (0.5019607843137255, 0.5019607843137255, 0.5019607843137255), 'honeydew': (0.9411764705882353, 1.0, 0.9411764705882353), 'hotpink': (1.0, 0.4117647058823529, 0.7058823529411765), 'indianred': (0.803921568627451, 0.3607843137254902, 0.3607843137254902), 'indigo': (0.29411764705882354, 0.0, 0.5098039215686274), 'ivory': (1.0, 1.0, 0.9411764705882353), 'khaki': (0.9411764705882353, 0.9019607843137255, 0.5490196078431373), 'lavender': (0.9019607843137255, 0.9019607843137255, 0.9803921568627451), 'lavenderblush': (1.0, 0.9411764705882353, 0.9607843137254902), 'lawngreen': (0.48627450980392156, 0.9882352941176471, 0.0), 'lemonchiffon': (1.0, 0.9803921568627451, 0.803921568627451), 'lightblue': (0.6784313725490196, 0.8470588235294118, 0.9019607843137255), 'lightcoral': (0.9411764705882353, 0.5019607843137255, 0.5019607843137255), 'lightcyan': (0.8784313725490196, 1.0, 1.0), 'lightgoldenrodyellow': (0.9803921568627451, 0.9803921568627451, 0.8235294117647058), 'lightgray': (0.8274509803921568, 0.8274509803921568, 0.8274509803921568), 'lightgreen': (0.5647058823529412, 0.9333333333333333, 0.5647058823529412), 'lightgrey': (0.8274509803921568, 0.8274509803921568, 0.8274509803921568), 'lightpink': (1.0, 0.7137254901960784, 0.7568627450980392), 'lightsalmon': (1.0, 0.6274509803921569, 0.47843137254901963), 'lightseagreen': (0.12549019607843137, 0.6980392156862745, 0.6666666666666666), 'lightskyblue': (0.5294117647058824, 0.807843137254902, 0.9803921568627451), 'lightslategray': (0.4666666666666667, 0.5333333333333333, 0.6), 'lightslategrey': (0.4666666666666667, 0.5333333333333333, 0.6), 'lightsteelblue': (0.6901960784313725, 0.7686274509803922, 0.8705882352941177), 'lightyellow': (1.0, 1.0, 0.8784313725490196), 'lime': (0.0, 1.0, 0.0), 'limegreen': (0.19607843137254902, 0.803921568627451, 0.19607843137254902), 'linen': (0.9803921568627451, 0.9411764705882353, 0.9019607843137255), 'magenta': (1.0, 0.0, 1.0), 'maroon': (0.5019607843137255, 0.0, 0.0), 'mediumaquamarine': (0.4, 0.803921568627451, 0.6666666666666666), 'mediumblue': (0.0, 0.0, 0.803921568627451), 'mediumorchid': (0.7294117647058823, 0.3333333333333333, 0.8274509803921568), 'mediumpurple': (0.5764705882352941, 0.4392156862745098, 0.8588235294117647), 'mediumseagreen': (0.23529411764705882, 0.7019607843137254, 0.44313725490196076), 'mediumslateblue': (0.4823529411764706, 0.40784313725490196, 0.9333333333333333), 'mediumspringgreen': (0.0, 0.9803921568627451, 0.6039215686274509), 'mediumturquoise': (0.2823529411764706, 0.8196078431372549, 0.8), 'mediumvioletred': (0.7803921568627451, 0.08235294117647059, 0.5215686274509804), 'midnightblue': (0.09803921568627451, 0.09803921568627451, 0.4392156862745098), 'mintcream': (0.9607843137254902, 1.0, 0.9803921568627451), 'mistyrose': (1.0, 0.8941176470588236, 0.8823529411764706), 'moccasin': (1.0, 0.8941176470588236, 0.7098039215686275), 'navajowhite': (1.0, 0.8705882352941177, 0.6784313725490196), 'navy': (0.0, 0.0, 0.5019607843137255), 'oldlace': (0.9921568627450981, 0.9607843137254902, 0.9019607843137255), 'olive': (0.5019607843137255, 0.5019607843137255, 0.0), 'olivedrab': (0.4196078431372549, 0.5568627450980392, 0.13725490196078433), 'orange': (1.0, 0.6470588235294118, 0.0), 'orangered': (1.0, 0.27058823529411763, 0.0), 'orchid': (0.8549019607843137, 0.4392156862745098, 0.8392156862745098), 'palegoldenrod': (0.9333333333333333, 0.9098039215686274, 0.6666666666666666), 'palegreen': (0.596078431372549, 0.984313725490196, 0.596078431372549), 'paleturquoise': (0.6862745098039216, 0.9333333333333333, 0.9333333333333333), 'palevioletred': (0.8588235294117647, 0.4392156862745098, 0.5764705882352941), 'papayawhip': (1.0, 0.9372549019607843, 0.8352941176470589), 'peachpuff': (1.0, 0.8549019607843137, 0.7254901960784313), 'peru': (0.803921568627451, 0.5215686274509804, 0.24705882352941178), 'pink': (1.0, 0.7529411764705882, 0.796078431372549), 'plum': (0.8666666666666667, 0.6274509803921569, 0.8666666666666667), 'powderblue': (0.6901960784313725, 0.8784313725490196, 0.9019607843137255), 'purple': (0.5019607843137255, 0.0, 0.5019607843137255), 'rebeccapurple': (0.4, 0.2, 0.6), 'red': (1.0, 0.0, 0.0), 'rosybrown': (0.7372549019607844, 0.5607843137254902, 0.5607843137254902), 'royalblue': (0.2549019607843137, 0.4117647058823529, 0.8823529411764706), 'saddlebrown': (0.5450980392156862, 0.27058823529411763, 0.07450980392156863), 'salmon': (0.9803921568627451, 0.5019607843137255, 0.4470588235294118), 'sandybrown': (0.9568627450980393, 0.6431372549019608, 0.3764705882352941), 'seagreen': (0.1803921568627451, 0.5450980392156862, 0.3411764705882353), 'seashell': (1.0, 0.9607843137254902, 0.9333333333333333), 'sienna': (0.6274509803921569, 0.3215686274509804, 0.17647058823529413), 'silver': (0.7529411764705882, 0.7529411764705882, 0.7529411764705882), 'skyblue': (0.5294117647058824, 0.807843137254902, 0.9215686274509803), 'slateblue': (0.41568627450980394, 0.35294117647058826, 0.803921568627451), 'slategray': (0.4392156862745098, 0.5019607843137255, 0.5647058823529412), 'slategrey': (0.4392156862745098, 0.5019607843137255, 0.5647058823529412), 'snow': (1.0, 0.9803921568627451, 0.9803921568627451), 'springgreen': (0.0, 1.0, 0.4980392156862745), 'steelblue': (0.27450980392156865, 0.5098039215686274, 0.7058823529411765), 'tan': (0.8235294117647058, 0.7058823529411765, 0.5490196078431373), 'teal': (0.0, 0.5019607843137255, 0.5019607843137255), 'thistle': (0.8470588235294118, 0.7490196078431373, 0.8470588235294118), 'tomato': (1.0, 0.38823529411764707, 0.2784313725490196), 'turquoise': (0.25098039215686274, 0.8784313725490196, 0.8156862745098039), 'violet': (0.9333333333333333, 0.5098039215686274, 0.9333333333333333), 'wheat': (0.9607843137254902, 0.8705882352941177, 0.7019607843137254), 'white': (1.0, 1.0, 1.0), 'whitesmoke': (0.9607843137254902, 0.9607843137254902, 0.9607843137254902), 'yellow': (1.0, 1.0, 0.0), 'yellowgreen': (0.6039215686274509, 0.803921568627451, 0.19607843137254902)}

# color palettes
{'viridis': [(0.267004, 0.004874, 0.329415, 1.0), (0.275191, 0.194905, 0.496005, 1.0), (0.214298, 0.355619, 0.551184, 1.0), (0.154815, 0.493313, 0.55784, 1.0), (0.120638, 0.625828, 0.533488, 1.0), (0.274149, 0.751988, 0.436601, 1.0), (0.595839, 0.848717, 0.243329, 1.0), (0.964894, 0.902323, 0.123941, 1.0)],
'plasma': [(0.050383, 0.029803, 0.527975, 1.0), (0.32515, 0.006915, 0.639512, 1.0), (0.54057, 0.03495, 0.64864, 1.0), (0.719181, 0.191729, 0.542663, 1.0), (0.853319, 0.351553, 0.413734, 1.0), (0.951344, 0.52285, 0.292275, 1.0), (0.994474, 0.722691, 0.174381, 1.0), (0.946602, 0.95519, 0.150328, 1.0)],
'jet': [(0.0, 0.0, 0.5, 1.0), (0.0, 0.06470588235294118, 1.0, 1.0), (0.0, 0.6294117647058823, 1.0, 1.0), (0.2371916508538899, 1.0, 0.7305502846299811, 1.0), (0.6925996204933585, 1.0, 0.27514231499051234, 1.0), (1.0, 0.7559912854030507, 0.0, 1.0), (1.0, 0.2331154684095862, 0.0, 1.0), (0.553475935828877, 0.0, 0.0, 1.0)],
'gist_rainbow': [(1.0, 0.0, 0.16, 1.0), (1.0, 0.6009538950715422, 0.0, 1.0), (0.6359300476947536, 1.0, 0.0, 1.0), (0.0, 1.0, 0.12650221378874135, 1.0), (0.0, 1.0, 0.8855154965211895, 1.0), (0.0, 0.34846547314578047, 1.0, 1.0), (0.4187979539641946, 0.0, 1.0, 1.0), (1.0, 0.0, 0.8139386189258311, 1.0)],
'rainbow': [(0.5, 0.0, 1.0, 1.0), (0.21764705882352942, 0.42912060877260894, 0.9755119679804366, 1.0), (0.06470588235294117, 0.7752039761111298, 0.9032471993461288, 1.0), (0.34705882352941175, 0.9712810319161138, 0.7867449380334832, 1.0), (0.6294117647058823, 0.9794097676013659, 0.631711006253251, 1.0), (0.9117647058823528, 0.7980172272802396, 0.4457383557765383, 1.0), (1.0, 0.4622038835403133, 0.2379351950426188, 1.0), (1.0, 0.03695149938914491, 0.018478904959129915, 1.0)],
'Set1': [(0.8941176470588236, 0.10196078431372549, 0.10980392156862745, 1.0), (0.21568627450980393, 0.49411764705882355, 0.7215686274509804, 1.0), (0.30196078431372547, 0.6862745098039216, 0.2901960784313726, 1.0), (0.596078431372549, 0.3058823529411765, 0.6392156862745098, 1.0), (1.0, 0.4980392156862745, 0.0, 1.0), (1.0, 1.0, 0.2, 1.0), (0.6509803921568628, 0.33725490196078434, 0.1568627450980392, 1.0), (0.9686274509803922, 0.5058823529411764, 0.7490196078431373, 1.0)],
'cvd_safe': []}




}



def regex_string(motif):
    """Function that returns a regular expression string to search for in the sequence from a motif."""
    motifstring = motif.strip()
    value_regex = "(?i)(?="
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
            value_regex = value_regex + "[" + i + "]"
    value_regex = value_regex + ")"
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
    """A function that takes in a fasta file object, and an empty dictionary, and populates the dictionary with the fasta headers as keys and a list of the fasta sequence and a scalar as the value. Returns the count of fasta entries."""
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
    return len(dictionary) # return count of fasta entries



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
color_step = int(255 / (motif_count - 1))
color_n = 0
for key in motif_dictionary:
    motif_dictionary[key].append(getattr(cm, colormap)(color_n))
    color_n = color_n + color_step

# Input FASTA file, count fasta entries
fasta_dict = {} # will contain fasta header as keys, with a list having the sequence and a scalar as the value
fasta_count = fasta_process(fastafile, fasta_dict) # also populates fasta_dict

# Initialize canvas
canvas_height = (fasta_count * 100) + 160 + (30 * motif_count)
img_filename = fastafile.split(".")[0] + "_motifs" + filetype

surface = cairo.SVGSurface(img_filename, 1100, canvas_height)
context = cairo.Context(surface)
context.set_source_rgb(0, 0, 0)
context.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
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
                context.set_source_rgba(1, 1, 1, 1)
                context.set_line_width(20)
                context.stroke()
            for i in motif_coords:
                context.move_to(50 + int(i * fasta_dict[key][1]), draw_strand)
                context.line_to(50 + int(i * fasta_dict[key][1]) + motif_len, draw_strand)
                context.set_source_rgba(motif_dictionary[x][1][0], motif_dictionary[x][1][1], motif_dictionary[x][1][2], .5)
                context.set_line_width(20)
                context.stroke()


    draw_line = draw_line + 100
surface.finish()
print(motif_dictionary)
