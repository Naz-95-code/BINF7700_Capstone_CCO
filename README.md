Universal Mutation Analysis Dashboard (UMAD)

Overview

The Universal Mutation Analysis Dashboard (UMAD) is a bioinformatics pipeline designed to process and analyze large collections of Variant Call Format (VCF) files from cancer genome datasets.

The goal of UMAD is to provide a reproducible workflow for mutation characterization, comparison across samples, and biological interpretation of mutation patterns.

The pipeline currently processes simulated cancer datasets (Breast Adenocarcinoma and Prostate Adenocarcinoma) and extracts key mutation metrics including mutation spectra, mutation burden, mutational signatures, and allele frequency distributions.

These analyses support the development of an interactive dashboard for exploring mutation patterns across cancer samples.

⸻

Current Implemented Modules

Mutation Spectrum Extraction
	•	Filters SNPs (Single Nucleotide Polymorphisms)
	•	Extracts mutation types (REF → ALT)
	•	Counts mutation occurrences
	•	Normalizes mutation frequencies
	•	Combines spectra across samples

Mutation Burden Analysis
	•	Calculates total mutations per sample
	•	Enables comparison of mutation loads across tumors

COSMIC Mutational Signature Analysis
	•	Identifies mutational signatures using combined spectra
	•	Generates signature exposure plots and heatmaps

Allele Frequency Analysis
	•	Extracts variant allele frequencies from VCF files using bcftools
	•	Supports analysis of mutation prevalence and tumor clonality

Project Structure

universal-mutation-analysis-dashboard/
│
├── scripts/
│   ├── extract_spectrum.sh
│   ├── combine_spectra.sh
│   └── extract_allele_frequency.sh
│
├── data/
│   ├── test/
│   └── full/
│
├── results/
│   ├── spectra/
│   ├── combined/
│   ├── allele_frequency/
│   └── cosmic_fit_output/
│
└── docs/

Requirements
	•	bcftools (v1.21)
	•	Linux command-line environment
	•	Python (for visualization)


Long-Term Vision

UMAD is being developed as a modular system that will support:
	•	Variant annotation
	•	Mutation signature profiling
	•	Cross-cancer comparison
	•	Statistical visualization
	•	Integration with interactive mutation analysis dashboards

