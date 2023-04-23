import sys 
import time
import os
import numpy as np
import gzip

print("starting now!\n")

# trios = map: child_id -> [father_id, mother_id]
trios = np.genfromtxt("id_files/relations_both_parents.txt", dtype=str, delimiter='\t', skip_header=1, autostrip=True)
trios = {x[0]:(x[1:]) for x in trios}
print(trios)

print("trios created!\n")

# pop_info = map: child_id -> [population_code, superpopulation_code]
pop_info = np.genfromtxt("igsr_samples.tsv", dtype=str, delimiter='\t', skip_header=1, usecols=(0,3,5), autostrip=True)
pop_info = {r[0]:r[1:] for r in pop_info if r[0] in trios}


print("pop_info created!\n")

#indir = "/home/amisra7/scratch16-rmccoy22/abortvi2/vcf_shapeit5/phased_T2T_panel/"
# files = [f for f in os.listdir(indir) if f[-3:] == ".gz"]

indir = ""
files = ["/home/amisra7/scratch16-rmccoy22/amisra7/filtering/1KGP_small.CHM13v2.0.chr22.recalibrated.snp_indel.pass.phased.vcf.gz"]

outdir = "/home/amisra7/scratch4-rmccoy22/amisra7/new_denovo_tsvs/"


def genotype_possible(child_gt, pa_gt, ma_gt):
    possible_genos = {pa_gt[:-1] + ma_gt[0], pa_gt[:-1] + ma_gt[-1], ma_gt[:-1] + pa_gt[0], ma_gt[:-1] + pa_gt[-1]}

    if child_gt in possible_genos or child_gt[::-1] in possible_genos:
        return True

    return False


columns = "\t".join(["#CHROM", "POS", "REF", "ALT", "CHILD_ID", "FATHER_ID", "MOTHER_ID", "CHILD_GT", "FATHER_GT", "MOTHER_GT", "POP", "SUPERPOP"])

for file in files:
    chr = file.split('.')[3]
    out_tsv = outdir + chr + '_all_sites.tsv'
    out_bed = outdir + chr + '_all_sites.bed'
    infile = indir + file

    if os.path.isfile(out_tsv):
        continue
    
    if not os.path.isfile(infile):
        print("error: %s not found!\n" % infile)

    print("starting data iteration for {0}!\n".format(chr))

    bed_sites = []

    with open(out_tsv, "w") as tsv_fp:
        tsv_fp.write(columns + '\n')

        with gzip.open(infile, mode="rt") as infp:

            while True:
                row = infp.readline().strip()
                
                if not row:
                    break
                
                if row[0] == '#':
                    if row[1] != '#':
                        row = row.split('\t')
                        header = {val: idx for idx, val in enumerate(row)}

                    continue
                
                row = row.split('\t')

                mutation_at_site = False

                for cid, parid in trios.items():
                    pid, mid = parid[0], parid[1]
                    cgt, pgt, mgt = row[header[cid]], row[header[pid]], row[header[mid]]

                    if genotype_possible(cgt, pgt, mgt):
                        continue
                    
                    mutation_at_site = True

                    line = row[0:2] + row[3:5] + [cid, pid, mid] + [cgt, pgt, mgt] + pop_info[cid].tolist()
                    
                    tsv_fp.write('\t'.join(line) + '\n')
                    
                if mutation_at_site:
                    bed_sites.append(row[1])
        
        print("finished tsv data iteration for {0}!\n".format(chr))
    
    with open(out_bed, "w") as bed_fp:
        [bed_fp.write("%s\t%s\t%s\n" % (chr, i, i)) for i in bed_sites]
    
    print("finished bed file data iteration for {0}!\n".format(chr))
                    

                
# make sure later, sort final out tsvs by pos column
# maybe add INFO field: can note down double mutants, places where parents are not hom-ref