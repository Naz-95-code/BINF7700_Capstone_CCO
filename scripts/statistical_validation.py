import pandas as pd
from scipy.stats import ks_2samp, spearmanr

# Load synthetic data
synthetic = pd.read_csv("../results/mutation_burden.tsv", sep="\t")
synthetic_counts = synthetic["total_mutations"]

# Load real TCGA data (WITH HEADERS)
real_breast = pd.read_csv("../data/full/Breast_Mutation_Count.txt", sep="\t")
real_prostate = pd.read_csv("../data/full/Prostate_Mutation_Count.txt", sep="\t")

# Extract correct column
real_counts = pd.concat([
    real_breast["Mutation Count"],
    real_prostate["Mutation Count"]
])

# KS test
ks_stat, ks_p = ks_2samp(synthetic_counts, real_counts)

# Match lengths for Spearman
min_len = min(len(synthetic_counts), len(real_counts))
synthetic_matched = synthetic_counts[:min_len]
real_matched = real_counts[:min_len]

# Spearman
corr, pval = spearmanr(synthetic_matched, real_matched)

# Output
print("\nStatistical Validation (Synthetic vs TCGA)")

print("\nKS Test")
print("KS Statistic:", ks_stat)
print("KS p-value:", ks_p)

print("\nSpearman Correlation")
print("Spearman Correlation:", corr)
print("Spearman p-value:", pval)
