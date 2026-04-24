import numpy as np
from scipy.stats import mannwhitneyu
import sys

def run_test(synthetic_file, real_file, cancer_type):
    # Load data
    synthetic = np.loadtxt(synthetic_file, skiprows=1, usecols=1)
    real = np.loadtxt(real_file, skiprows=1, usecols=3, delimiter="\t")

    n1, n2 = len(synthetic), len(real)

    # Run test
    stat, p_value = mannwhitneyu(synthetic, real, alternative='two-sided')

    # Effect size (rank-biserial correlation)
    r = 1 - (2 * stat) / (n1 * n2)
    r_abs = abs(r)

    if r_abs >= 0.5:
        magnitude = "Large"
    elif r_abs >= 0.3:
        magnitude = "Medium"
    elif r_abs >= 0.1:
        magnitude = "Small"
    else:
        magnitude = "Negligible"

    # Output
    print(f"\nMann-Whitney U Test — {cancer_type}")
    print("=" * 40)
    print(f"n synthetic:  {n1}")
    print(f"n real:       {n2}")
    print(f"Statistic:    {stat:.4f}")
    print(f"P-value:      {p_value:.2e}")
    print(f"Effect size r: {r:.4f} ({magnitude})")

    if p_value < 0.05:
        print("Result: Distributions are significantly different")
    else:
        print("Result: No significant difference")

# --- Run for both cancer types ---
run_test(
    synthetic_file="results/breast_mutation_burden.tsv",
    real_file="data/full/tcga_breast_mutation_counts.txt",
    cancer_type="Breast"
)

run_test(
    synthetic_file="results/prostate_mutation_burden.tsv",
    real_file="data/full/tcga_prostate_mutation_counts.txt",
    cancer_type="Prostate"
)
