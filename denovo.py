import sys 
import time
import os
import numpy as np

print("starting now!\n")

# trios = map: child_id -> [father_id, mother_id]
trios = np.genfromtxt("id_files/relations.txt", dtype=str, delimiter='\t', skip_header=1, autostrip=True)
trios = {x[0]:x[1:] for x in trios}


print("trios created!\n")

# pop_info = map: child_id -> [population_code, superpopulation_code]
pop_info = np.genfromtxt("igsr_samples.tsv", dtype=str, delimiter='\t', skip_header=1, usecols=(0,3,5), autostrip=True)
pop_info = {r[0]:r[1:] for r in pop_info if r[0] in trios}


print("pop_info created!\n")


def genotype_possible(row, child_allele, parent):
    if parent == "0":
        return True, "./."
    
    parent_gt = row[header[parent]]

    # child allele at phasing location doesnt match either of corresponding parent alleles
    if child_allele != parent_gt[0] and child_allele != parent_gt[-1]:
        return False, parent_gt

    return True, parent_gt


indir = "/home/amisra7/scratch16-rmccoy22/abortvi2/vcf_phasing_array/chm13_phased_vcf_header_fixed/"
files = os.listdir(indir)
outdir = "/home/amisra7/scratch16-rmccoy22/amisra7/denovo_tsvs/"

for file in files:
    chr = file.split('_')[0]
    outfile = outdir + chr + '_variants.tsv'
    
    if os.path.isfile(outfile):
        continue
    
    infile = indir + file

    print("starting data iteration for {0}!\n".format(chr))
    # outfile = "test.txt"
    with open(outfile, "w") as out_fp:
        columns = ["#CHROM", "POS", "REF", "ALT", "CHILD_ID", "FATHER_ID", "MOTHER_ID", "CHILD_GT", "FATHER_GT", "MOTHER_GT", "POP", "SUPERPOP"]
        out_fp.write('\t'.join(columns) + '\n')

        with open(infile, "r") as in_fp:

            while True:
                row = in_fp.readline().strip()

                if not row:
                    break

                if row[0] == '#':
                    if row[1] != "#":
                        row = row.split('\t')
                        header = {val: idx for idx, val in enumerate(row)}
                        # print(header)
                        # break
                    continue
                    

                # row = row.split('\t')

                # for child, parents in trios.items():
                #     child_gt = row[header[child]]

                #     poss_pa, pa_gt = genotype_possible(row, child_gt[0], parents[0])
                #     poss_ma, ma_gt = genotype_possible(row, child_gt[-1], parents[1])

                #     if poss_pa and poss_ma:
                #         continue

                #     line = row[0:2] + row[3:5] + [child] + parents.tolist() + [child_gt, pa_gt, ma_gt] + pop_info[child].tolist()
                #     out_fp.write('\t'.join(line) + '\n')
        break
    
    print("finished with data iteration for {0}!\n".format(chr))
            

print("finished all chromosomes variant identification!\n")

