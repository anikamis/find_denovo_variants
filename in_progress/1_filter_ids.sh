#!/bin/bash

# vcf files
# ~/scratch16-rmccoy22/abortvi2/vcf_phasing_array/chm13_phased_vcf_header_fixed/*.vcf

# family files
# ~/scratch16-rmccoy22/abortvi2/vcf_phasing_array/shapeit_out_recoded/*.sample
# ID_1 = family ID, ID_2 = individual ID;

#vcftools --remove ind.txt --vcf test.vcf --recode --out outtest.vcf
# ID_1 ID_2 missing father mother sex plink_pheno
# 0 0 0 0 0 0 -9
# 0 HG00096 0 0 0 1 -9
# 0 HG00097 0 0 0 2 -9
# 0 HG00099 0 0 0 2 -9
# 0 HG00100 0 0 0 2 -9
# 0 HG00101 0 0 0 1 -9

# input="/home/amisra7/scratch16-rmccoy22/abortvi2/vcf_phasing_array/shapeit_out_recoded/chr5_fam.sample"
# unrelated="unrelated_ids.txt"
# related="related_ids.txt"
# all="all_ids.txt"

# USAGE: ./1_filter_ids.sh -s <input vcf sample file> -o <output directory to write id files to>
# script will create three files in desired output directory: unrelated_ids.txt, related_ids.txt, and all_ids.txt
# each file contains ids of all unrelated individuals, related individuals, and all individuals respectively

# parse arguments
while getopts i:o: flag
do
    case "${flag}" in
        i) input=${OPTARG};;
        o) outdir=${OPTARG%/};;
    esac
done


unrelated=$outdir"/unrelated_ids.txt"
related=$outdir"/related_ids.txt"
all=$outdir"/all_ids.txt"


# yield output files containing all individual ids, all unrelated individual ids, and all related individual ids
while IFS= read -r line || [ -n "$line" ]; do
    read -a arr <<< $line

    if [ "${arr[0]}" == "ID_1" ] || [ ${arr[1]} == 0 ]; then
        continue;
    fi

    if [ ${arr[3]} == 0 ] && [ ${arr[4]} == 0 ];
    then
        echo "${arr[1]}" >> "$unrelated"
    else
        echo "${arr[1]}" >> "$related"
    fi

    echo "${arr[1]}" >> "$all"

done < "$input"