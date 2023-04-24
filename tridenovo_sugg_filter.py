import os


input_path = "/home/amisra7/scratch4-rmccoy22/amisra7/orig_denovo_tsvs/"
#                     0         1      2      3       4            5             6            7          8            9         10        11        12
header = "\t".join(["#CHROM", "POS", "REF", "ALT", "CHILD_ID", "FATHER_ID", "MOTHER_ID", "CHILD_GT", "FATHER_GT", "MOTHER_GT", "POP", "SUPERPOP", "INFO"])


# return 1 if parents are NOT both homo-ref
# return 2 if child is double mutant
# return 3 if both
# return 0 if neither
def unusual_mutations(child, father, mother):
    ret = 0
    par_alleles = {father[0], father[-1], mother[0], mother[-1]}

    if par_alleles != {"0"}:
        ret += 1
    
    if child[0] not in par_alleles and child[-1] not in par_alleles:
        ret += 2

    return ret


# def make_freqs(data):
#     freqs = defaultdict(lambda: list([0, dict()]))

#     for row in data:
#         alts = ",".split(row[3])
#         cgt = row[7]
#         print(cgt)

#         if cgt[0] != "0":
#             freqs[row[1]][1][alts[int(cgt[0]) - 1]] += 1
        
#         if cgt[-1] != "0":
#             freqs[row[1]][1][alts[int(cgt[-1]) - 1]] += 1
        
#         freqs[row[1]][0] += 6
    
#     return freqs



omit_unusual_mutations = True
omit_several_alts = True
omit_ac = True
ac = 1
omit_allele_fq = True
afq = 0.002

for i in range(1, 23)[::-1]:
    chr = "chr" + str(i)
    indir = input_path + chr + "/"

    infile = indir + chr + "_denovo_filtered.tsv"
    outfile = indir + chr + "_denovo_tdn_filtered.tsv"

    if os.path.isfile(outfile):
        continue
    print(infile, outfile)
    with open(infile, "r") as infp:
        with open(outfile, "w") as outfp:
            pos_to_skip = -1
            last_pos = -1
            last_pos_rows = []

            while True:
                row = infp.readline().strip()
                if not row:
                    break
                data = row.split()
                if data[0][0] == '#' or data[1] == pos_to_skip:
                    continue
                if data[1] != last_pos
                    if len(last_pos_rows) <= ac:
                        #outfp.writelines(last_pos_rows)
                        last_pos_rows = []

                last_pos = data[1]
                last_pos_rows.append(row)
                
                # only keep sites w single alt and sites w homo-ref parents and single mutant child
                if len(data[3].split(',')) > 1 or unusual_mutations(*(data[7:10])) != 0:
                    pos_to_skip = data[1]
                    pos_count = 0
                    continue
            
    print("finished chr" + str(i))
    break




    # data = np.genfromtxt(infile, dtype=str, delimiter="\t", skip_header=1, autostrip=True)

    # if omit_several_alts and omit_unusual_mutations:
    #     data = np.array([x for x in data if len(x[3]) > 1 and unusual_mutations(*(x[7:10])) == 0])
    # elif omit_several_alts:
    #     data = np.array([x for x in data if len(x[3]) > 1])
    # elif omit_unusual_mutations:
    #     data = np.array([x for x in data if unusual_mutations(*(x[7:10])) == 0])
    
    # make counter from pos column. since here, were assuming that were onyl considering sites with one alt allele, and
    # all parents must be homo-ref, and all children can be at most single mutant (therefore heteroref), we can omit sites
    # that have more than ac rows worht of occurrences
    # if omit_ac:
    #     freqs = Counter(data[:,1])
    #     data = np.array([x for x in data if freqs[x[1]] <= ac])

    # np.savetxt(outfile, data, fmt="%s", delimiter="\t", newline="\n", header=header)
    # print("finished with chr" + str(i))


    # freqs = make_freqs(data)
    # print("freqs table made for chr" + str(i))
    # outdata = []

    # if omit_ac or omit_allele_fq:
    #     for row in data:
    #         # for now, only implementing ac
    #         pos, alt = row[1], row[3].split(",")
    #         # assume child is ref/alt heterozygous
    #         child_alt = row[7].split("|")[0] if row[7][1] == "0" else row[7].split("|")[1]
    #         alt_allele = alt[int(child_alt) - 1]

    #         if freqs[pos][1][alt_allele] > ac:
    #             continue
                
    #         outdata.append(row)
    
    # outdata = np.array(outdata)
    # np.savetxt(outfile, outdata, delimiter="\t", newline="\n", header=header)
    # print("finished with chr" + str(i))
    # break









