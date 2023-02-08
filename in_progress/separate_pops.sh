#!/bin/bash

mkdir -p separated/populations
pops=($( ls ~/scratch16-rmccoy22/amisra7/vcf_phasing/pop_info/csvs/ ))

# create all population directories
for p in "${pops[@]}"
do
    pop="${p%%.*}"
    mkdir separated/populations/"$pop"
done


mkdir -p separated/chromosomes
vcfs=($( ls ~/scratch16-rmccoy22/amisra7/vcf_phasing/vcf_unrelated/*.vcf ))

# run bcftools split on each chromosome vcf file
for i in "${files[@]}"
do
    fname="${i##*/}"
    chr="${fname%%_*}"

    outdir=separated/chromosomes/"$chr"
    mkdir "$outdir"

    bcftools +split "$i" -o "$outdir" -G pop_info/all_info.tsv

    cd "$outdir"
    
    # prepend chromosome name to each population file name
    for FNAME in *; do mv $FNAME "$chr"_$FNAME; done
    cd ..

done

# move all files from being separated by chromosome to being separated by pop
cd separated/populations

for DNAME in *; do mv ../chromosomes/*/*_$DNAME.vcf $DNAME/. ; done
cd ../..