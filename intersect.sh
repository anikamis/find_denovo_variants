#!/bin/bash

indir="/home/amisra7/scratch4-rmccoy22/amisra7/denovo_tsvs/"
dirs=($( ls $indir ))

outfile="denovo_bed_sites.bed"

for i in "${dirs[@]}"
do
    filename=$indir"$i"/"$i"_denovos.tsv
    sites=($( awk 'BEGIN{FS=OFS="\t"}  NR > 1 { print $2 }' $filename | sort -u  ))

    for j in "${sites[@]}"
    do
        echo -e "$i""\t""$j""\t""$j" >> $outfile
    done
    echo "$i completed!"
done

#awk 'BEGIN{FS=OFS="\t"} {print>$1"_good_sites.bed"}' filtered_dn_sites.bed 