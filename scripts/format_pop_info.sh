#!/bin/bash

# sed 's/,/\t/g' pop_info/ACB.csv | awk -v d="-" 'BEGIN{FS=OFS="\t"}{$2=d}2' > test/ACB.final.tsv
# bcftools +split test.vcf -o testdir -G pop_info/all_info.tsv

# reformat population csv files to be in bcftools input format

final=~/scratch16-rmccoy22/amisra7/vcf_phasing/pop_info/all_info.tsv

files=($( ls ~/scratch16-rmccoy22/amisra7/vcf_phasing/pop_info/csvs/*.csv ))

for i in "${files[@]}"
do
    fname="${i##*/}"
    pop="${fname%%.*}"
    out=~/scratch16-rmccoy22/amisra7/vcf_phasing/pop_info/tsvs/"$pop".corrected.tsv

    # change csv to tsv and reformat such that tsv is "ID - POP" to be in bcftools +split -G input format
    sed 's/,/\t/g' "$i" | awk -v d="-" 'BEGIN{FS=OFS="\t"}{t=$1; $1=$3; $2=d; $3=t; print }' > "$out"
    cat "$out" >> "$final"
done