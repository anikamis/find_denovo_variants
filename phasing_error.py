import sys 
import time
import os
import numpy as np

# infile = "chr22_variants.tsv"
# infile = "chr22_variants_short.tsv"

def poss_phasing_err(child_gt, pa_gt, ma_gt):
    # homo = lambda gt : gt[0] == gt[-1]

    # # child only has one parent in database
    # if pa_id == '0' or ma_id == '0':
    #     parent_gt = pa_gt if ma_id == '0' else ma_gt

    #     # parent and child are each homozygous opposites
    #     if homo(child_gt) and homo(parent_gt) and child_gt[0] != parent_gt[0]:
    #         return False
        
    #     return True
    
    possible_genos = {pa_gt[:-1] + ma_gt[0], pa_gt[:-1] + ma_gt[-1], ma_gt[:-1] + pa_gt[0], ma_gt[:-1] + pa_gt[-1]}

    if child_gt in possible_genos or child_gt[::-1] in possible_genos:
        return True

    return False


header = "\t".join(["#CHROM", "POS", "REF", "ALT", "CHILD_ID", "FATHER_ID", "MOTHER_ID", "CHILD_GT", "FATHER_GT", "MOTHER_GT", "POP", "SUPERPOP"])

indir = "/home/amisra7/scratch4-rmccoy22/amisra7/denovo_tsvs/"
files = os.listdir(indir)

for file in files:
    if len(file) < 4 or file[-4:] != ".tsv":
        continue
    
    print("beginning to split {0}!\n".format(indir + file))
    chr = file.split('_')[0]

    outdir = indir + chr + '/'

    os.mkdir(outdir)

    error_data = []
    novel_data = []

    error_out = chr + "_phasing_errors.tsv"
    novel_out = chr + "_denovos.tsv"

    infile = indir + file

    with open(infile, "r") as fp:
        while True:
            line = fp.readline().strip()

            if not line:
                break
            elif line[0] == '#':
                continue
            
            data = line.split('\t')

            # omit "trios" with only one parent
            if data[5] == '0' or data[6] == '0':
                error_data.append(line)
            
            elif poss_phasing_err(*data[7:10]):
                error_data.append(line)
            
            else:
                novel_data.append(line)


    np.savetxt(outdir + error_out, error_data, fmt='%s', newline='\n', header=header, comments='')
    np.savetxt(outdir + novel_out, novel_data, fmt='%s', newline='\n', header=header, comments='')
    
    os.rename(infile, outdir + file)
    print("done splitting {0}!\n".format(indir + file))



print("done splitting all chromosomes!")
