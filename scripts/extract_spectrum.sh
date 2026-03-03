#!/bin/bash

set -e

module load bcftools/1.21

# Check argument
if [ -z "$1" ]; then
    echo "Usage: bash scripts/extract_spectrum.sh <vcf_directory>"
    exit 1
fi

input_dir=$1
output_dir="results/spectra"

mkdir -p "$output_dir"

for file in "$input_dir"/*.vcf.gz
do
    echo "Processing $file"

    filename=$(basename "$file" .vcf.gz)

    bcftools view -v snps "$file" | \
    bcftools query -f '%REF>%ALT\n' | \
    sort | uniq -c | \
    awk '
    {
        total += $1
        counts[$2] = $1
    }
    END {
        for (type in counts)
            printf "%s\t%d\t%.6f\n", type, counts[type], counts[type]/total
    }' \
    > "$output_dir/${filename}_spectrum.txt"

done

echo "Done."
