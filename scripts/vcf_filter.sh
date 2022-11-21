#!/bin/bash

# bcftools view --output out.test.vcf -S unrelated_ids.txt test.vcf 
# vcftools --vcf test.vcf --out out.test --remove related_ids.txt

# call vcftools on every chromosome vcf to filter out all related individuals
files=($( ls ~/scratch16-rmccoy22/abortvi2/vcf_phasing_array/chm13_phased_vcf_header_fixed/*.vcf ))

for i in "${files[@]}"
do
    fname="${i##*/}"
    chr="${fname%%_*}"

    if [ "$chr" == "chr10" ] || [ "$chr" == "chr11" ] || [ "$chr" == "chr13" ] || [ "$chr" == "chr14" ] || [ "$chr" == "chr15" ] || [ "$chr" == "chr17" ];
    then
        continue
    fi

    echo "Starting $chr!"

    out=~/scratch16-rmccoy22/amisra7/vcf_phasing/vcf_unrelated/"$chr"_unrelated_phased

    vcftools --vcf "$i" --out "$out" --remove related_ids.txt --recode

    echo "Finished $chr!"

done