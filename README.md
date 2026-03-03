# Universal Mutation Analysis Dashboard (UMAD)

## Overview

The Universal Mutation Analysis Dashboard (UMAD) is a scalable bioinformatics pipeline designed to process and analyze large collections of Variant Call Format (VCF) files.

The goal of UMAD is to provide a reproducible framework for mutation characterization, comparison across samples, and downstream statistical interpretation.

This repository currently implements the mutation spectrum extraction module.


## Current Implemented Module

### Mutation Spectrum Extraction

This module:

- Filters SNPs (Single Nucleotide Polymorphisms)
- Extracts mutation types (REF > ALT)
- Computes mutation counts
- Normalizes counts to proportions
- Combines spectra across multiple samples

## Project Structure

```
universal-mutation-analysis-dashboard/
│
├── scripts/              # Shell scripts for mutation spectrum analysis
│   ├── extract_spectrum.sh
│   └── combine_spectra.sh
│
├── data/
│   ├── test/             # Small test VCF files
│   └── full/             # Full dataset (80+ VCF files)
│
├── results/
│   ├── spectra/          # Per-sample mutation spectra
│   └── combined/         # Combined comparison tables
│
└── docs/                 # Documentation and notes
```

## Requirements

- bcftools (v1.21)
- Linux command-line environment


## Long-Term Vision

UMAD is being developed as a modular system that will support:

- Variant annotation
- Mutation signature profiling
- Cross-cancer comparison
- Statistical visualization
- Integration with interactive dashboards


