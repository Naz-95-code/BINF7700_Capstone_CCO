#!/bin/bash
module load bcftools

INPUT_DIR="../data/full"
OUTPUT_DIR="../results/variant_types"

mkdir -p $OUTPUT_DIR

for file in $INPUT_DIR/*/*.vcf.gz
do
    sample=$(basename $file .vcf.gz)

    echo "Processing $sample"

    bcftools view -H $file | awk '
    {
        ref=$4
        alt=$5

        if(length(ref)==1 && length(alt)==1)
            type="SNP"
        else
            type="INDEL"

        print type
    }' | sort | uniq -c > $OUTPUT_DIR/${sample}_variant_types.txt

done
