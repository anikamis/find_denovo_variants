import sys 
import time
import os
import numpy as np
import gzip
from collections import defaultdict

input_path = "/home/amisra7/scratch4-rmccoy22/amisra7/orig_denovo_tsvs/"
#                     0         1      2      3       4            5             6            7          8            9         10        11        12
header = "\t".join(["#CHROM", "POS", "REF", "ALT", "CHILD_ID", "FATHER_ID", "MOTHER_ID", "CHILD_GT", "FATHER_GT", "MOTHER_GT", "POP", "SUPERPOP", "INFO"])


# return 1 if parents are NOT both homo-ref
# return 2 if child is double mutant
# return 3 if both
# return 0 if neither
def unusual_mutations(child, father, mother):
    ret = 0
    par_alleles = set(father[0], father[-1], mother[0], mother[-1])

    if par_alleles != {"0"}:
        ret += 1
    
    if child[0] not in par_alleles and child[-1] not in par_alleles:
        ret += 2

    return ret


def make_freqs(data):
    freqs = defaultdict([0, dict])

    for row in data:
        alts = ",".split(row[3])
        cgt = row[7]

        if cgt[0] != "0":
            freqs[row[1]][1][alts[int(cgt[0]) - 1]] += 1
        
        if cgt[-1] != "0":
            freqs[row[1]][1][alts[int(cgt[-1]) - 1]] += 1
        
        freqs[row[1]][0] += 6
    
    return freqs

omit_unusual_mutations = True
omit_several_alts = True
omit_ac = True
ac = 3
omit_allele_fq = True
afq = 0.002

for i in range(1, 23):
    chr = "chr" + str(i)
    indir = input_path + chr + "/"

    infile = indir + chr + "_denovo_filtered.tsv"
    outfile = indir + chr + "_denovo_tdn_filtered.tsv"

    data = np.genfromtxt(infile, dtype=str, delimiter="\t", skip_header=1, autostrip=True)

    if omit_several_alts:
        data = np.array([x for x in data if len(x[3]) > 1])
    
    if omit_unusual_mutations:
        data = np.array([x for x in data if unusual_mutations(*(x[7:10])) == 0])
    
    freqs = make_freqs(data)

    outdata = []

    if omit_ac or omit_allele_fq:
        for row in data:
            pos, alt
            if omit_ac:








