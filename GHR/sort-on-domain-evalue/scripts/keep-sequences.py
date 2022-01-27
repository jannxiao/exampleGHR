#! python

###headerfile format: XXXXXX\n so on and so forth
###fastafile format: >XXXXXXX\nyyyyyyyy\nyyyyyyyyyy\n so on and so forth

import sys
headerfilename = sys.argv[1]
fastafilename = sys.argv[2]
newfastafilename = sys.argv[3]
mode = ""

#>human-TRPA_TRPA1_TRPA1-uniprotO75762-TRPA1_HUMAN-Himmel2020_extraction_687_1001_8.2e-208 True
if (len(sys.argv) > 4):
    mode = sys.argv[4]
    keyword = sys.argv[5]
    header_ends = {}

headerfile = open(headerfilename,'r')
headerlist = []
for header in headerfile:
    if (mode != "") and (header[:-1].split('\t')[-1] == 'True'):
        info = header.split('\t')[0].split('_')
        header = '_'.join(info[:-4])
        header_ends[header] = info[-4:]
    if header[0] != '>':
        headerlist.append('>'+header.rstrip())
    else:
        headerlist.append(header.rstrip())
headerfile.close()

fastafile = open(fastafilename,'r')
sequencedict = {}
for nextline in fastafile:
    if nextline[0] == '>':
        header = nextline[:-1]
        if header in headerlist:
            sequencedict[header] = ''
    else:
        if header in sequencedict:
            sequencedict[header] += nextline[:-1]
fastafile.close()

newfastafile = open(newfastafilename,'w')
for header in sequencedict:
    if mode !=  "":
        if keyword not in header:
            info = header_ends[header]
            start, end, evalue = int(info[-3]), int(info[-2]), info[-1]
            #tail = '_' + '_'.join(info)
            tail = '_extraction_'+str(start)+'_'+str(end)
            if mode == 'convertmode_extracted':
                #newfastafile.write(header+tail+'\n')
                #newfastafile.write(sequencedict[header][start-1:end]+'\n')
                newfastafile.write(header+tail+'\n')
                newfastafile.write(sequencedict[header][start-1:end]+'\n')
            elif mode == 'convertmode_full':
                #newfastafile.write(header+'_'+evalue+'\n')
                #newfastafile.write(sequencedict[header]+'\n')
                newfastafile.write(header+'\n')
                newfastafile.write(sequencedict[header]+'\n')
    else:
        newfastafile.write(header+'\n')
        newfastafile.write(sequencedict[header]+'\n')
newfastafile.close()

