#! python

# 6-diamond-report-human_TRPA1_X_human-genome
# /scratch2/eedsinger/projects/sono/phylogenomics/whale/ancestral-sequences/projectdb-gene-sets/projectdb-fastas/projectdb-Balaena-mysticetus
# human-TRPA1-uniprot_O75762      Homo-sapiens-gdb10007535aa      0.0e+00 2095.5
import sys

###### BEING SCRIPT 
# read in reference gene header identifier and sequence into dictionary
rgs_seq = {}
input_rgsfasta = open( sys.argv[3], 'r' )
for next_line in input_rgsfasta:
    if next_line[ 0 ] == '>':
        identifier = next_line[ 1:-1 ].split( ' ' )[ 0 ]
        rgs_seq[ identifier ] = ''
    else:
        rgs_seq[ identifier ] = rgs_seq[ identifier ] + next_line[ :-1 ]
input_rgsfasta.close()
        
# read rgs query and rgs genome top hit into dictionary
gengene_refgene = {}
rgs_genes = []
gengenes = []
    
model_species = sys.argv[6]
input_report = open( sys.argv[1], 'r' )
for next_hit in input_report:
    info = next_hit.split( '\t' )
    refgene = info[ 0 ]
    gengene = info[ 1 ]
    if model_species in refgene:
        if (refgene not in rgs_genes) and (gengene not in gengenes):
            gengene_refgene[ gengene ] = refgene
            rgs_genes.append( refgene )
            gengenes.append( gengene )
input_report.close()


# read in RGS genome and replace rgs genes (top hit in blast of rgs _X_ rgs genome) with rgs header and sequence
header_seq = {}

input_fasta = open( sys.argv[2], 'r' )
output_map = open( sys.argv[4], 'w' )
output_name = sys.argv[5] 
print(output_name)
output_fasta = open( output_name, 'w' )



seqdict = {}
for nextline in input_fasta:
    if nextline[0] == '>':
        header = nextline[1:-1]
        seqdict[header] = ""
    else:
        seqdict[header] += nextline[:-1]

for header in seqdict:
    if header in gengene_refgene:
        gengene = header
        refgene = gengene_refgene[ gengene ]
        sequence = rgs_seq[ refgene ]
        output_fasta.write( '>' + refgene + '\n')
        output_fasta.write( sequence + '\n' )
        output_map.write( gengene + '\t' + refgene + '\n' )
    else:
        output_fasta.write('>' + header + '\n')
        output_fasta.write(seqdict[header] + '\n')



#for next_line in input_fasta:
#    if next_line[ 0 ] == '>':
#        count = 0
#        header_info = next_line[ 1:-1 ]
#        if header_info in gengene_refgene.keys():
#            count = 1
#            gengene = header_info
#            refgene = gengene_refgene[ gengene ]
#            header = '>' + refgene + '\n'
#            output_fasta.write( header )
#            output = gengene + '\t' + refgene + '\n'
#            output_map.write( output )                
#        else:
#            header = next_line
#            output_fasta.write( header )
#    else:
#        if count == 0:
#            sequence = next_line
#            output_fasta.write( sequence )
#        else:
#            sequence = rgs_seq[ refgene ] + '\n'
#            output_fasta.write( sequence )

input_fasta.close()
output_fasta.close()
output_map.close()



