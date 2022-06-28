#!/bin/sh

#gen_tissue-expression_files.sh rna_tissue_hpa.tsv.zip tissue-filtered_interactomes/
tissue_exp_zipf=$1
out_folder=$2

tissue_expf="${filename%.*}.gz"

unzip -p $tissue_exp_zipf "${tissue_exp_zipf%.*}" | gzip >$tissue_expf
zcat $tissue_expf | tail -n+2 | cut -f3 | sort -u >tissues
#tissue="adipose tissue"
while read tissue
do
	tissue_exp="$out_folder${tissue/ /_}.tsv"
	echo "Saving expression info of \"$tissue\" into: $tissue_exp"
	zgrep "$tissue" $tissue_expf |cut -f2,6 >$tissue_exp
done <tissues
