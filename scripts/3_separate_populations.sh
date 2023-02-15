#!/bin/bash

# USAGE: ./3_separate_populations.sh -p <path/to/tsv/from/igsr/website>
#                                    -i <directory containing output from step 2>
#                                    -o <desired output directory for all vcfs separated by population>

# TODO: this can be deleted once rockfish starts working again
# TODO: but for now, set command alias to path of cloned bcftools repo
bcftools=/home/amisra7/scratch16-rmccoy22/amisra7/filtering/bcftools/bcftools
export BCFTOOLS_PLUGINS=/home/amisra7/scratch16-rmccoy22/amisra7/filtering/bcftools/plugins

# parse arguments
usage() { echo "$0 usage:" && grep " .)\ #" $0; exit 0; }

[ $# -eq 0 ] && usage
while getopts "hp:i:o:" arg; do
    case $arg in
        p) # -t <location of tsv sourced from https://www.internationalgenome.org/data-portal/sample > "Download the list">
            raw_tsv=${OPTARG}
            ;;
        i) # -i <directory containing phased vcf files of all chromosomes for unrelated individuals (step 2 output dir)>
            indir=${OPTARG%/}
            ;;
        o) # -o <<desired output directory for sorted output vcf files for each population>
            outdir=${OPTARG%/}
            ;;            
        h | *)
            usage
            exit 0
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;

        :)
            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
  esac
done


workdir="$outdir"/working
mkdir -p "$workdir"

# generate tsv file of input format desired by bcftools +split -G option
groups="$workdir"/group_file.tsv
awk 'BEGIN{FS=OFS="\t"} NR>1 { printf "%s\t%s\t%s\n", $1, "-", $4 }' $raw_tsv > $groups

# create output directory for each population in study
popnames=($( awk 'BEGIN{FS=OFS="\t"} { print $3 }' $groups | sort -u ))
for population in "${popnames[@]}"; do mkdir -p $outdir/$population ; done

# loop over all vcf files in input directory
# vcfs=($( ls $indir/*.vcf ))

for i in "${vcfs[@]}"
do
    # isolate name of chromosome from filename for later
    chr="${i##*/}"
    chr="${chr%%_*}"

    echo "Starting $chr!"
    # run bcftools split plugin with -G option
    # will output one vcf per population into "working" directory
    bcftools +split $i -o $workdir -Ov -G $groups 2>$workdir/error.log

    # rename output vcf files by prepending chromosome to filename
    # and moving to respective population folder
    for f in $workdir/*.vcf; do pop=$( echo -e "$f" | sed 's\.*/\\;s\[.].*\\' ); mv $f $outdir/$pop/"$chr"_$pop.vcf ; done

    echo "Finished sorting $chr by population!"
done

rm -rf "$workdir"

echo "All chromosomes complete!"
