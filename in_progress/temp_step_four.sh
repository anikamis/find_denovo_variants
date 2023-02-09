#!/bin/bash

outdir=/home/amisra7/scratch16-rmccoy22/amisra7/filtering/vcf_populations/test_outdir
outdir="${outdir%/}"
# when taking input, rememeber to strip last slash if exists ${INPUT%/}
workdir="$outdir"/working
mkdir -p "$workdir"

orig_pop_info=/home/amisra7/scratch16-rmccoy22/amisra7/filtering/vcf_populations/pop_info/orig_info.tsv

groupfn="$workdir"/group_info.tsv

echo "Created group file!"

awk 'BEGIN{FS=OFS="\t"} NR>1 { printf "%s\t%s\t%s\n", $1, "-", $4 }' $orig_pop_info > $groupfn

popnames=($( awk 'BEGIN{FS=OFS="\t"} { print $3 }' $groupfn | sort -u ))

for pop in "${popnames[@]}"
do
    #pop="${p%%.*}"
    mkdir -p $outdir/$pop
done

echo "Created all population directories!"

indir=/home/amisra7/scratch16-rmccoy22/amisra7/filtering/vcf_populations/in_vcfs/
indir="${indir%/}"

vcfs=($( ls $indir/*.vcf ))

for i in "${vcfs[@]}"
do
    chr="${i##*/}"
    chr="${chr%%_*}"

    chrgroupfn=$workdir/group_info_$chr.tsv

    awk -v chr=$chr 'BEGIN{FS=OFS="\t"} { printf "%s\t%s\t%s_%s\n", $1, $2, chr, $3 }' $groupfn > $chrgroupfn

    # bcftools +split "$i" -o "$workdir" -Ov -G "$chrgroupfn" 2>/dev/null
    bcftools +split $i -o $workdir -Ov -G $chrgroupfn 2>$workdir/error.log

    for f in $workdir/chr*.vcf; do pop=$( echo -e "$f" | sed 's\.*/\\;s\_.*\\' ); mv $f $outdir/$pop/. ; done

    rm $chrgroupfn

    echo "Finished sorting $chr by population!"
done

#rm -rf "$workdir"

echo "All chromosomes complete!"
