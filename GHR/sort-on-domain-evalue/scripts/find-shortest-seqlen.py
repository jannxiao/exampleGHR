#! python
import sys

#filename = '../userinput/worm-trpl-proteins-05jun2021-pore_regions.fasta'
filename = '../1-process-fastas/refseq-pore.fasta'

inputfasta = open(filename,'r')
print("\nchecking ",filename)
sequences = {}
for nextline in inputfasta:
    if nextline[0] == '>':
        header = nextline[1:-1]
        sequences[header] = ""
    else:
        sequences[header] += nextline[:-1]

minlen = sys.maxsize
minheader = ""
for header in sequences:
    sequence = sequences[header]
    if len(sequence) < minlen:
        minlen = len(sequence)
        minheader = header
print("Shortest seq is ",minheader)
print("Shortest len:",minlen)
print("\nDon't forget to take buffer length into account!\n")

