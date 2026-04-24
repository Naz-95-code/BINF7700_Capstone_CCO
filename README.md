# Universal VCF Mutation Analysis Dashboard (UMAD)

## Overview

The **Universal VCF Mutation Analysis Dashboard (UMAD)** is a bioinformatics pipeline designed to process and analyze large collections of **Variant Call Format (VCF)** files from cancer genome datasets.

The goal of UMAD is to provide a **reproducible workflow for mutation characterization, comparison across samples, and biological interpretation of mutation patterns**, in both OncoGAN synthetic and TCGA real data.

The pipeline currently processes simulated cancer datasets (**Breast Adenocarcinoma** and **Prostate Adenocarcinoma**)

These analyses support the development of an **interactive dashboard for exploring mutation patterns across cancer samples**.

## Key Objectives

- Evaluate the biological realism of OncoGAN-generated genomes
- Compare mutation patterns between OncoGAN synthetic and real cancer datasets
- Validate biological plausibility using COSMIC mutational signatures
- Quantify differences in mutation burden and variability
- Provide an interactive dashboard for exploration and interpretation

## Data Sources

- Synthetic Data: OncoGAN-generated VCF files
- Real Data: TCGA (Breast and Prostate cancer datasets)
- Reference: COSMIC Single Base Substitution (SBS) signature
### 1. Mutation Burden Analysis

- Computes total mutations per sample
- Compares distributions between synthetic and real datasets
- Statistical testing using Mann–Whitney U test
- Effect size (r) used to quantify magnitude of differences

### 2. Mutation Spectrum

- Classifies SNVs into six base substitution types
- Generates normalized mutation spectra
- Evaluates dominant mutation patterns (e.g., C>T transitions)

### 3. COSMIC Signature Analysis

- Extracts mutational signatures from combined spectra
- Compares against COSMIC reference signatures
- Generates heatmaps and exposure plots
- Assesses biological fidelity of synthetic data

## Project Structure

```
BINF7700_Capstone_CCO/
│
├── dashboard.py
├── README.md
├── requirements.txt
│
├── src/
│   ├── plot_heatmap.py
│   ├── plot_mutation_burden.py
│   ├── plot_mutation_spectrum.py
│   ├── plot_cosine_similarity.py
│   ├── mann_whitney_test.py
│   ├── biological_validation.py
│
├── scripts/
│   ├── extract_spectrum.sh
│   ├── combine_spectra.sh
│   ├── combine_variant_types.sh
│   ├── classify_variants.sh
│
├── data/
│
├── results/
│   ├── spectra/
│   ├── combined/
│   └── cosmic_fit_output/
│
├── figures/
│
└── docs/

```

```
BINF7700_Capstone_CCO/
├── dashboard.py
├── README.md
├── requirements.txt
│
├── src/                  # Core analysis logic
├── scripts/              # Helper shell scripts
│
├── data/                 # Input data
├── results/              # Processed outputs
├── figures/              # Final visualizations
│
├── logs/
├── docs/
└── cosmic_fit_output/

```
## Methods

1. Mutation Burden

* Defined as total number of mutations per sample
* Log transformation applied to handle skewed distributions
* Compared between synthetic and real data

2. Statistical Analysis

* Mann-Whitney U test used to compare mutation distributions
* Rank-biserial correlation used to measure effect size

3. Mutation Spectrum

* Computed frequency of base substitutions (e.g., C>T, C>A)
* Used to identify dominant mutation patterns

4. Mutational Signatures

* COSMIC SBS signatures extracted and normalized
* Key signatures identified (SBS1, SBS5, SBS40, etc.)

5. Similarity Analysis

* Cosine similarity used to compare mutation profiles to COSMIC references

## Requirements
- bcftools (v1.21+) 
- Python 3.x 
- Linux environment (HPC recommended) 

### Python Libraries
- pandas 
- numpy 
- scipy 
- plotly 
- streamlit 


## Key Findings
- OncoGAN data reproduces **COSMIC mutational signatures**, supporting biological plausibility 
- Mutation spectra show consistent dominance of known patterns (e.g., C>T transitions) 
- OncoGAN samples exhibit:
  - Higher mutation burden 
  - Reduced variability 
- Real datasets show:
  - Greater heterogeneity 
  - Broader mutation distributions 

These results highlight both the **strengths and limitations of synthetic cancer genomes**.

## Dashboard

The Streamlit dashboard provides:

* Mutation burden visualization
* Mutation spectrum analysis
* COSMIC signature heatmaps
* Cosine similarity comparison
* Summary and interpretation

## How to Run

```bash
git clone https://github.com/Naz-95-code/BINF7700_Capstone_CCO.git
cd BINF7700_Capstone_CCO
conda activate vcf_env
pip install -r requirements.txt
streamlit run dashboard.py

## Author
Chinazo Christella Orji 
M.Sc. Bioinformatics 
Northeastern University, Toronto.



