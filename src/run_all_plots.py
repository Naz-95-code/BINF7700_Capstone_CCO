import os
import subprocess

print("Generating all plots...\n")

# Ensure figures folder exists
os.makedirs("figures", exist_ok=True)

commands = [
    [
        "python", "scripts/plot_histogram.py",
        "data/txt/synthetic_breast_counts.txt",
        "figures/synthetic_breast_histogram.png",
        "OncoGAN Breast Mutation Burden"
    ],
    [
        "python", "scripts/plot_histogram.py",
        "data/txt/synthetic_prostate_counts.txt",
        "figures/synthetic_prostate_histogram.png",
        "OncoGAN Prostate Mutation Burden"
    ],
    [
        "python", "scripts/plot_histogram.py",
        "data/txt/real_breast_counts.txt",
        "figures/real_breast_histogram.png",
        "TCGA Breast Mutation Burden"
    ],
    [
        "python", "scripts/plot_histogram.py",
        "data/txt/real_prostate_counts.txt",
        "figures/real_prostate_histogram.png",
        "TCGA Prostate Mutation Burden"
    ]
]

for cmd in commands:
    subprocess.run(cmd, check=True)

print("\nAll plots saved in figures/")
