
#!/usr/bin/env python3
# A script to turn a FASTA file into a phylip file.

fasta = open("fish_astns.fasta", "r")
#fasta = open("small_multiline_test.fa", "r")
sequence =""
counter = 0
for line in fasta:
    line = line.strip()

    if counter == 0: # special case for first loop through
        header = line
        print(header)
        counter = counter + 1

    elif line[0] == ">": # this works for all except very first one
        print(sequence) # as soon as hit the next header line print stored sequence
        sequence = "" # clear the sequence
        header = line
        print(header) # print the header

    else: # store the sequence
        sequence = sequence + line

print(sequence) # print the last sequence
fasta.close()
