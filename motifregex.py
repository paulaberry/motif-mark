#!/usr/bin/env python3
def motifreg(motif):
    """make regex search string out of motif"""
    letters=list(motif)
    value_regex = "(?i"
    for letter in letters:
        if letter == "T" or letter == "t" or letter == "U" or letter == "u":
            reg.append("[TU]")
        elif letter == "M" or letter == "m":
            reg.append("[AC]")
        elif letter == "R" or letter == "r":
            reg.append("[AG]")
        elif letter == "W" or letter == "w":
            reg.append("[AT]")
        elif letter == "S" or letter == "s":
            reg.append("[CG]")
        elif letter == "Y" or letter == "y":
            reg.append("[CT]")
        elif letter == "K" or letter == "k":
            reg.append("[GT]")
        elif letter == "V" or letter == "v":
            reg.append("[ACG]")
        elif letter == "H" or letter == "h":
            reg.append("[ACT]")
        elif letter == "D" or letter == "d":
            reg.append("[AGT]")
        elif letter == "B" or letter == "b":
            reg.append("[CGT]")
        elif letter == "N" or letter == "n":
            reg.append("[AGCTUN]")
        else:
            reg.append(letter)
    regtext=''.join(reg)
    return(regtext)
