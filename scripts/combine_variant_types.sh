#!/bin/bash
module load bcftools

INPUT_DIR="../results/variant_types"
OUTPUT_FILE="../results/variant_type_summary.tsv"

echo -e "Sample\tSNP\tINDEL" > $OUTPUT_FILE

for file in $INPUT_DIR/*_variant_types.txt
do
    sample=$(basename $file _variant_types.txt)

    snp=$(grep SNP $file | awk '{print $1}')
    indel=$(grep INDEL $file | awk '{print $1}')

    echo -e "${sample}\t${snp}\t${indel}" >> $OUTPUT_FILE
done

echo "Variant summary table created:"
echo $OUTPUT_FILE
