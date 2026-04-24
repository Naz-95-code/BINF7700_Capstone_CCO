import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure output folder exists
os.makedirs("results/figures", exist_ok=True)

def plot_burden(syn_file, real_file, cancer_type, output):

    # --- Load synthetic data ---
    syn = pd.read_csv(syn_file, sep="\t")
    syn_counts = syn.iloc[:, 1]   # second column = mutation counts

    # --- Load TCGA real data ---
    real = pd.read_csv(real_file, sep="\t")
    real_counts = real.iloc[:, -1]  # last column = mutation count

    # --- Plot ---
    plt.figure(figsize=(8,6))

    sns.histplot(
        syn_counts,
        color="blue",
        label="OncoGAN",
        kde=True,
        stat="density",
        bins=30,
        alpha=0.5
    )

    sns.histplot(
        real_counts,
        color="red",
        label="TCGA",
        kde=True,
        stat="density",
        bins=30,
        alpha=0.5
    )

    plt.title(f"{cancer_type} Mutation Burden: OncoGAN vs TCGA")
    plt.xlabel("Mutation Burden")
    plt.ylabel("Density")
    plt.legend()

    plt.tight_layout()
    plt.savefig(output, dpi=300)
    plt.close()


# Breast
plot_burden(
    syn_file="data/synthetic/breast_mutation_burden.tsv",
    real_file="data/real/tcga_breast_mutation_counts.txt",
    cancer_type="Breast",
    output="results/figures/breast_burden_comparison.png"
)

# Prostate
plot_burden(
    syn_file="data/synthetic/prostate_mutation_burden.tsv",
    real_file="data/real/tcga_prostate_mutation_counts.txt",
    cancer_type="Prostate",
    output="results/figures/prostate_burden_comparison.png"
)
