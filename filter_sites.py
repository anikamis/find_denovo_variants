import sys 
import time
import os
import numpy as np

header = "\t".join(["#CHROM", "POS", "REF", "ALT", "CHILD_ID", "FATHER_ID", "MOTHER_ID", "CHILD_GT", "FATHER_GT", "MOTHER_GT", "POP", "SUPERPOP"])

indir = "/home/amisra7/scratch4-rmccoy22/amisra7/denovo_tsvs/"
dirs = os.listdir(indir)

for chr in dirs:

    print("beginning to filter {0}!\n".format(chr))

    dir = indir + chr + '/'

    infn = dir + chr + "_denovos.tsv"
    inbed = dir + chr + "_good_sites.bed"
    outfn = dir + chr + "_denovo_filtered.tsv"

    if os.path.isfile(outfn):
        continue

    good_sites = set(np.genfromtxt(inbed, dtype=int, delimiter="\t", skip_header=0, usecols=(1), autostrip=True))

    with open(outfn, "w") as out_fp:
        with open(infn, "r") as in_fp:

            while True:
                row = in_fp.readline().strip()

                if not row:
                    break
                
                if row[0] == '#':
                    out_fp.write(row + '\n')
                    continue
                
                pos = int(row.split('\t')[1])

                if pos not in good_sites:
                    continue
                
                out_fp.write(row + '\n')

    print("finished with filtering {0}!\n".format(chr))

print("finished filtering all chromosomes!")