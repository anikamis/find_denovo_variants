import sys 
import numpy as np

# trios = map: child_id -> [father_id, mother_id]
trios = np.genfromtxt("id_files/relations.txt", dtype=str, delimiter='\t', skip_header=1, autostrip=True)
trios = {x[0]:x[1:] for x in trios}

# pop_info = map: child_id -> [population_code, superpopulation_code]
pop_info = np.genfromtxt("igsr_samples.tsv", dtype=str, delimiter='\t', skip_header=1, usecols=(0,3,5), autostrip=True)
pop_info = {r[0]:r[1:] for r in pop_info if r[0] in trios}

# header = map: individual_id -> index in header
# vcf data = genotype data from vcf
vcf_data = np.genfromtxt("../chr21_small_phased_headerCat.vcf", dtype=str, delimiter='\t', comments="##", autostrip=True)
header, vcf_data = {val: idx for idx, val in enumerate(vcf_data[0])}, vcf_data[1:]


def genotype_possible(row, child_allele, parent):
    if parent == "0":
        return True, "./."
    
    parent_gt = row[header[parent]]

    # child allele at phasing location doesnt match either of corresponding parent alleles
    if child_allele != parent_gt[0] and child_allele != parent_gt[-1]:
        return False, parent_gt

    return True, parent_gt

outfile = "variants.tsv"



with open(outfile, "w") as fp:
    columns = ["#CHROM", "POS", "REF", "ALT", "CHILD_ID", "FATHER_ID", "MOTHER_ID", "CHILD_GT", "FATHER_GT", "MOTHER_GT", "POP", "SUPERPOP"]
    fp.write('\t'.join(columns) + '\n')

    for row in vcf_data:

        for child, parents in trios.items():
            child_gt = row[header[child]]

            poss_pa, pa_gt = genotype_possible(row, child_gt[0], parents[0])
            poss_ma, ma_gt = genotype_possible(row, child_gt[-1], parents[1])

            if poss_pa and poss_ma:
                continue

            # line = row[0:2].tolist() + row[3:5].tolist() + [child] + parents + [child_gt, pa_gt, ma_gt] + pop_info[child]
            line = row[0:2].tolist() + row[3:5].tolist() + [child] + parents.tolist() + [child_gt, pa_gt, ma_gt] + pop_info[child].tolist()
            fp.write('\t'.join(line) + '\n')
        


