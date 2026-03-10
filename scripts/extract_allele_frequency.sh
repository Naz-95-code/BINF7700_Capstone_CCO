#!/bin/bash
set -e

input_root="data/full"
output_dir="results/allele_frequency"

mkdir -p "$output_dir"

module load bcftools/1.21

for cancer in Breast-AdenoCa Prost-AdenoCA
do
    echo "Processing cancer type: $cancer"

    for file in "$input_root/$cancer"/*.vcf.gz
    do
        sample=$(basename "$file" .vcf.gz)

        echo "Processing sample: $sample"

        bcftools query -f '%AF\n' "$file" \
            > "$output_dir/${sample}_af.txt"

    done

done

echo "Allele frequency extraction complete"
